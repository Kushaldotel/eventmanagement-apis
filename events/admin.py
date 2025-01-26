from django.contrib import admin
from django import forms
import json
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Event, Category, FAQ, Speaker
from django.db import models

# ---------------------------
# FAQ Admin
# ---------------------------
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'event', 'order')
    list_filter = ('event',)
    search_fields = ('question', 'answer')
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }

# ---------------------------
# Speaker Admin
# ---------------------------
class SpeakerForm(forms.ModelForm):
    class Meta:
        model = Speaker
        fields = '__all__'
        widgets = {
            'bio': CKEditor5Widget(config_name='extends'),
            'socials': forms.Textarea(attrs={'rows': 3})
        }

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    form = SpeakerForm
    list_display = ('name', 'event', 'designation', 'organization')
    list_filter = ('event',)
    search_fields = ('name', 'bio', 'designation')
    readonly_fields = ('photo_preview',)

    fieldsets = (
        (None, {
            'fields': (
                'event',
                'name',
                'photo',
                'photo_preview',
                'designation',
                'organization'
            )
        }),
        ('Details', {
            'fields': (
                'bio',
                'socials',
                'order'
            )
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return admin.utils.mark_safe(
                f'<img src="{obj.photo.url}" style="max-height: 200px; max-width: 200px;" />'
            )
        return "No photo"
    photo_preview.short_description = 'Preview'
# ---------------------------
# FAQ Admin Configuration
# ---------------------------
class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = ('question', 'answer', 'order')
    formfield_overrides = {
        models.TextField: {  # Changed from forms.TextField to models.TextField
            'widget': CKEditor5Widget(config_name='extends')
        }
    }


# ---------------------------
# Speaker Admin Configuration
# ---------------------------
class SpeakerForm(forms.ModelForm):
    class Meta:
        model = Speaker
        fields = '__all__'
        widgets = {
            'bio': CKEditor5Widget(config_name='extends'),
            'socials': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': '{"twitter": "https://...", "linkedin": "https://..."}'
            }),
        }

    def clean_socials(self):
        socials = self.cleaned_data.get('socials')
        if socials:
            try:
                json.loads(socials)
            except json.JSONDecodeError:
                raise forms.ValidationError("Invalid JSON format. Example: {'twitter':'https://...'}")
        return socials

class SpeakerInline(admin.StackedInline):
    form = SpeakerForm
    model = Speaker
    extra = 1
    fields = (
        'name',
        'photo',
        'designation',
        'organization',
        'bio',
        'socials',
        'order'
    )

# ---------------------------
# Event Admin Configuration
# ---------------------------
class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'description': CKEditor5Widget(config_name='extends'),
            'short_description': CKEditor5Widget(config_name='extends')
        }

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    inlines = [FAQInline, SpeakerInline]
    list_display = (
        'title',
        'start_date',
        'location',
        'featured',
        'is_registration_open'
    )
    filter_horizontal = ('categories',)
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Basic Info', {
            'fields': (
                'title',
                'slug',
                'description',
                'short_description',
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
                'phone',
                'email'
            )
        }),
        ('Registration', {
            'fields': (
                'registration_deadline',
                'max_participants',
                'registration_fee',
                'event_fee',
                'is_registration_open'
            )
        }),
    )

# ---------------------------
# Category Admin
# ---------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')