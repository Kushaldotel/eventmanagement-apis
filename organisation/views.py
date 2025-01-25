from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Organization
from .serializers import OrganizationSerializer

class OrganizationDetailView(APIView):

    def get(self, request):

        try:
            organization = Organization.objects.first()
            if not organization:
                return Response({'message': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = OrganizationSerializer(organization, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)