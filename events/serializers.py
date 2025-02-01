from rest_framework import serializers
from .models import Event, Category, FAQ, Speaker, EventDay, EventSession, PolicyDocument, GeneralFAQ, Purchase
import json
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'order']

class SpeakerSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    banner_photo_url = serializers.SerializerMethodField()
    class Meta:
        model = Speaker
        fields = [
            'name',
            'bio',
            'photo_url',
            'banner_photo_url',
            'address',
            'phone',
            'email',
            'designation',
            'organization',
            'socials',
            'order'
        ]

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.photo and hasattr(obj.photo, 'url'):
            return request.build_absolute_uri(obj.photo.url)
        return None

    def get_banner_photo_url(self, obj):
        request = self.context.get('request')
        if obj.banner_photo and hasattr(obj.banner_photo, 'url'):
            return request.build_absolute_uri(obj.banner_photo.url)
        return None

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     # Convert socials JSON string to Python dict
    #     if instance.socials:
    #         representation['socials'] = json.loads(instance.socials)
    #     else:
    #         representation['socials'] = None
    #     return representation
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class EventSessionSerializer(serializers.ModelSerializer):
    speakers = SpeakerSerializer(many=True, read_only=True)

    class Meta:
        model = EventSession
        fields = [
            'start_time',
            'end_time',
            'title',
            'description',
            'session_type',
            'speakers',
            'location',
            'notes'
        ]

class EventDaySerializer(serializers.ModelSerializer):
    sessions = EventSessionSerializer(many=True, read_only=True)

    class Meta:
        model = EventDay
        fields = ['date', 'title', 'sessions']

class EventSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    featured_image_url = serializers.SerializerMethodField()
    faqs = FAQSerializer(many=True, read_only=True)
    speakers = SpeakerSerializer(many=True, read_only=True)
    days = EventDaySerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'start_date',
            'end_date',
            'location',
            'address',
            'phone',
            'email',
            'categories',
            'featured',
            'featured_image_url',
            'registration_deadline',
            'max_participants',
            'registration_fee',
            'event_fee',
            'is_registration_open',
            'created_at',
            'updated_at',
            'short_description',
            'faqs',
            'speakers',
            'days'
        ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    def get_featured_image_url(self, obj):
        request = self.context.get('request')
        if obj.featured_image and hasattr(obj.featured_image, 'url'):
            return request.build_absolute_uri(obj.featured_image.url)
        return None

class PolicyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyDocument
        fields = '__all__'

class GeneralFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralFAQ
        fields = [
            'id',
            'question',
            'answer',
            'category',
            'order',
            'created_at'
        ]


class PurchaseEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'event_fee', 'is_registration_open',
            'start_date', 'end_date', 'location'
        ]

class PurchaseSerializer(serializers.ModelSerializer):
    event = PurchaseEventSerializer(read_only=True)

    class Meta:
        model = Purchase
        fields = [
            'id', 'event', 'customer_name', 'customer_email',
            'amount_paid', 'is_paid', 'created_at'
        ]