from django.contrib import admin
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Event, Category

class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'description': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'},
                config_name='extends'
            )
        }

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = (
        'title',
        'start_date',
        'location',
        'featured',
        'registration_fee',
        'is_registration_open',
        'created_at'
    )
    list_filter = (
        'featured',
        'categories',
        'start_date',
        'is_registration_open'
    )
    search_fields = (
        'title',
        'description',
        'location',
        'address',
        'email'
    )
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)
    date_hierarchy = 'start_date'

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title',
                'slug',
                'description',
                'categories',
                'featured',
                'featured_image'
            )
        }),
        ('Event Details', {
            'fields': (
                'start_date',
                'end_date',
                'location',
                'address',
                ('phone', 'email'),
            )
        }),
        ('Registration Info', {
            'fields': (
                'registration_deadline',
                'max_participants',
                'registration_fee',
                'event_fee',
                'is_registration_open'
            )
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug',)
    search_fields = ('name',)