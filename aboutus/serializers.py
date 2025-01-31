from rest_framework import serializers
from .models import AboutUsSection, TeamMember, ContactSubmission
from django.core.mail import send_mail
from django.conf import settings

class TeamMemberSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = [
            'name',
            'position',
            'bio',
            'photo_url',
            'social_links',
            'order'
        ]

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.photo and hasattr(obj.photo, 'url'):
            return request.build_absolute_uri(obj.photo.url)
        return None

class AboutUsSectionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    team_members = TeamMemberSerializer(many=True, read_only=True)

    class Meta:
        model = AboutUsSection
        fields = [
            'title',
            'slug',
            'section_type',
            'content',
            'image_url',
            'video_url',
            'order',
            'is_active',
            'team_members'
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = '__all__'  # Include all fields

    def create(self, validated_data):
        # Save the submission
        contact_submission = ContactSubmission.objects.create(**validated_data)

        # Send an email notification
        subject = validated_data['subject']
        message = f"Name: {validated_data['name']}\nEmail: {validated_data['email']}\n\nMessage:\n{validated_data['message']}"
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Replace with your email
            [settings.EMAIL_HOST_USER],  # List of recipients
            fail_silently=False,
        )

        return contact_submission