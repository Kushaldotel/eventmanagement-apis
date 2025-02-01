from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, PolicyDocumentViewSet, GeneralFAQListView, CreatePaymentIntentView, StripeWebhookView

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'policies', PolicyDocumentViewSet, basename='policy')

urlpatterns = [
    path('', include(router.urls)),
    path('faqs/', GeneralFAQListView.as_view(), name='general-faqs'),
    path('api/events/<int:event_id>/create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('api/stripe/webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
]