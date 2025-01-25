from rest_framework import serializers
from .models import Event, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']

class EventSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    featured_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
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