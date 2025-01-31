from django import forms
from django.utils.html import format_html
from django_ckeditor_5.widgets import CKEditor5Widget
from django.contrib import admin
from .models import AboutUsSection, TeamMember, ContactSubmission
from django.db import models
from unfold.admin import ModelAdmin, StackedInline, TabularInline


class TeamMemberInline(TabularInline):
    model = TeamMember
    extra = 1
    fields = ('name', 'position', 'photo', 'order')
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }

@admin.register(AboutUsSection)
class AboutUsSectionAdmin(ModelAdmin):
    list_display = ('title', 'section_type', 'order', 'is_active')
    list_filter = ('section_type', 'is_active')
    search_fields = ('title', 'content')
    inlines = [TeamMemberInline]
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slug',
                'section_type',
                'content',
                'image',
                'video_url',
                'order',
                'is_active'
            )
        }),
    )

@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ('name', 'position', 'section', 'order')
    list_filter = ('section',)
    search_fields = ('name', 'position')
    readonly_fields = ('photo_preview',)

    fieldsets = (
        (None, {
            'fields': (
                'section',
                'name',
                'position',
                'photo',
                'photo_preview',
                'bio',
                'social_links',
                'order'
            )
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px;" />',
                obj.photo.url
            )
        return "No photo"
    photo_preview.short_description = 'Preview'

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'email',
                'subject',
                'message',
            )
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )