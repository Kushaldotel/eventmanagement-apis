from django.contrib import admin
from django import forms
import json
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Event, Category, FAQ, Speaker, EventDay, EventSession, PolicyDocument
from django.db import models
# from django.contrib.admin import TabularInline, StackedInline
from unfold.admin import ModelAdmin, StackedInline, TabularInline
# ---------------------------
# FAQ Admin
# ---------------------------
@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
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
class SpeakerAdmin(ModelAdmin):
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
                'banner_photo',
                'address',
                'phone',
                'email',
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

    # def clean_socials(self):
    #     socials = self.cleaned_data.get('socials')
    #     if socials:
    #         try:
    #             json.loads(socials)
    #         except json.JSONDecodeError:
    #             raise forms.ValidationError("Invalid JSON format. Example: {'twitter':'https://...'}")
    #     return socials

class SpeakerInline(StackedInline):
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

class EventSessionInline(TabularInline):
    model = EventSession
    extra = 1
    fields = ('start_time', 'end_time', 'title', 'session_type', 'speakers', 'location', 'day', 'description', 'notes')
    autocomplete_fields = ['speakers']

class EventDayInline(StackedInline):
    model = EventDay
    extra = 1
    fields = ('date', 'title')
    inlines = [EventSessionInline]
    show_change_link = True

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
class EventAdmin(ModelAdmin):
    form = EventAdminForm
    inlines = [EventDayInline,FAQInline, SpeakerInline]
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
class CategoryAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

@admin.register(EventDay)
class EventDayAdmin(ModelAdmin):
    list_display = ('date', 'event', 'title')
    list_filter = ('event',)
    # inlines = [EventSessionInline]
    search_fields = ('event__title', 'title')

@admin.register(EventSession)
class EventSessionAdmin(ModelAdmin):
    list_display = ('title', 'day', 'start_time', 'end_time', 'session_type')
    list_filter = ('session_type', 'day__event')
    search_fields = ('title', 'description')
    autocomplete_fields = ['speakers', 'day']

@admin.register(PolicyDocument)
class PolicyDocumentAdmin(ModelAdmin):
    list_display = ('document_type', 'title', 'version',)
    list_filter = ('document_type',)
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }

    fieldsets = (
        (None, {
            'fields': (
                'document_type',
                'title',
                'slug',
                'content',
                'version',
            )
        }),
        ('Metadata', {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )