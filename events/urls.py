from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, PolicyDocumentViewSet, GeneralFAQListView

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'policies', PolicyDocumentViewSet, basename='policy')

urlpatterns = [
    path('', include(router.urls)),
    path('faqs/', GeneralFAQListView.as_view(), name='general-faqs'),
]