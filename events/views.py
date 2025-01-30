from rest_framework import viewsets
from .models import Event, PolicyDocument
from .serializers import EventSerializer, PolicyDocumentSerializer, CategorySerializer, FAQSerializer, SpeakerSerializer

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