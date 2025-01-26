from rest_framework import viewsets
from .models import AboutUsSection, TeamMember
from .serializers import AboutUsSectionSerializer

class AboutUsSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AboutUsSection.objects.filter(is_active=True).prefetch_related('team_members')
    serializer_class = AboutUsSectionSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        section_type = self.request.query_params.get('type', None)
        if section_type:
            queryset = queryset.filter(section_type=section_type)
        return queryset.order_by('order')