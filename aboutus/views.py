from rest_framework import viewsets, generics
from .models import AboutUsSection, TeamMember, ContactSubmission
from .serializers import AboutUsSectionSerializer, TeamMemberSerializer, ContactSubmissionSerializer
from rest_framework.response import Response
from rest_framework import status

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

class ContactSubmissionCreateView(generics.CreateAPIView):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Your message has been sent successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)