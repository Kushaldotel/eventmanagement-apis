from rest_framework import viewsets
from .models import Event, PolicyDocument, GeneralFAQ, Purchase
from .serializers import EventSerializer, PolicyDocumentSerializer, CategorySerializer, FAQSerializer, SpeakerSerializer, GeneralFAQSerializer
from rest_framework.generics import ListAPIView
import stripe
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.core.mail import send_mail

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all().prefetch_related(
        'categories',
        'faqs',
        'speakers'
    ).order_by('-start_date')
    serializer_class = EventSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Add any filters here if needed (e.g., featured only)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class PolicyDocumentViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = PolicyDocument.objects.all()
    serializer_class = PolicyDocumentSerializer
    lookup_field = 'slug'

    def get_queryset(self):

        queryset = super().get_queryset()
        doc_type = self.request.query_params.get('type',None)
        if doc_type:
            queryset = queryset.filter(document_type=doc_type)
        return queryset


class GeneralFAQListView(ListAPIView):
    serializer_class = GeneralFAQSerializer

    def get_queryset(self):
        queryset = GeneralFAQ.objects.filter(is_active=True)

        # Optional category filtering
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__iexact=category)

        return queryset.order_by('order')



stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)

            # Create a PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(event.event_fee * 100),  # Convert to cents
                currency='usd',
                metadata={
                    'event_id': event.id,
                    'customer_name': request.data.get('customer_name'),
                    'customer_email': request.data.get('customer_email'),
                },
            )

            return Response(
                {
                    'clientSecret': intent.client_secret,
                    'event': EventSerializer(event).data
                },
                status=status.HTTP_200_OK
            )
        except Event.DoesNotExist:
            return Response(
                {'error': 'Event not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse(status=400)

        # Handle the event
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
            self.handle_payment_success(payment_intent)

        return HttpResponse(status=200)

    def handle_payment_success(self, payment_intent):
        # Save purchase details
        event = Event.objects.get(id=payment_intent.metadata.event_id)
        Purchase.objects.create(
            event=event,
            customer_name=payment_intent.metadata.customer_name,
            customer_email=payment_intent.metadata.customer_email,
            amount_paid=payment_intent.amount / 100,  # Convert back to dollars
            stripe_payment_intent_id=payment_intent.id,
            is_paid=True,
        )

        # Send confirmation email
        self.send_confirmation_email(event, payment_intent.metadata.customer_email)

    def send_confirmation_email(self, event, customer_email):
        subject = f"Purchase Confirmation: {event.title}"
        message = f"""
        Thank you for purchasing a ticket to {event.title}!

        Event Details:
        - Date: {event.start_date.strftime('%Y-%m-%d')}
        - Location: {event.location}

        We look forward to seeing you there!
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[customer_email],
            fail_silently=False,
        )