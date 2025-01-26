from rest_framework import serializers
from .models import AboutUsSection, TeamMember

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