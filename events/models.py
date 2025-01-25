from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,blank=True, max_length=200)
    description = CKEditor5Field('Description', config_name='extends')
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