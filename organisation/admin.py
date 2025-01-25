from django.contrib import admin
from .models import Organization

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_email", "contact_phone", "created_at", "updated_at")
    search_fields = ("name", "contact_email")
    readonly_fields = ("created_at", "updated_at")
