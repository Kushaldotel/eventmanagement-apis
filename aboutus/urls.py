from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AboutUsSectionViewSet

router = DefaultRouter()
router.register(r'all-sections', AboutUsSectionViewSet, basename='aboutus')

urlpatterns = [
    path('', include(router.urls)),
]