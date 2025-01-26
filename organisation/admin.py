from django.contrib import admin
from .models import Organization
from unfold.admin import ModelAdmin
@admin.register(Organization)
class OrganizationAdmin(ModelAdmin):
    list_display = ("name", "contact_email", "contact_phone", "created_at", "updated_at")
    search_fields = ("name", "contact_email")
    readonly_fields = ("created_at", "updated_at")
