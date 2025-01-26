from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import json

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,blank=True, max_length=200)
    description = CKEditor5Field('Description', config_name='extends')
    short_description = CKEditor5Field('Short Description', config_name='extends', null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default=False)
    featured_image = models.ImageField(upload_to='events/featured/')
    registration_deadline = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2)
    event_fee = models.DecimalField(max_digits=10, decimal_places=2)
    is_registration_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-start_date']

class FAQ(models.Model):

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=200)
    answer = CKEditor5Field('Answer', config_name='extends')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"FAQ: {self.question}"

class Speaker(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='speakers')
    name = models.CharField(max_length=100)
    bio = CKEditor5Field('Bio', config_name='extends')
    photo = models.ImageField(upload_to='speakers/', null=True, blank=True)
    designation = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, blank=True)
    socials = models.JSONField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def clean(self):
        super().clean()
        if self.socials:
            try:
                json.loads(self.socials)
            except json.JSONDecodeError:
                raise ValidationError({'socials': 'Invalid JSON format'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name