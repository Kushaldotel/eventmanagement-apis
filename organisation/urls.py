from django.urls import path
from .views import OrganizationDetailView

urlpatterns = [
    path('detail/', OrganizationDetailView.as_view(), name='organization'),
]
