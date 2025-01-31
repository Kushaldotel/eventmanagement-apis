from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AboutUsSectionViewSet, ContactSubmissionCreateView

router = DefaultRouter()
router.register(r'aboutus', AboutUsSectionViewSet, basename='aboutus')

urlpatterns = [
    path('', include(router.urls)),
    path('contact/', ContactSubmissionCreateView.as_view(), name='contact-form'),
]