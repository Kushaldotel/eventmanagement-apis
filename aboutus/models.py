from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify

class AboutUsSection(models.Model):
    SECTION_TYPES = (
        ('HERO', 'Hero Section'),
        ('MISSION', 'Mission Statement'),
        ('TEAM', 'Team Members'),
        ('HISTORY', 'Our History'),
        ('VALUES', 'Core Values'),
        ('STATS', 'Statistics'),
        ('PARTNERS', 'Partners'),
        ('CTA', 'Call to Action'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    content = CKEditor5Field('Content',config_name='extends')
    image = models.ImageField(upload_to='about_us/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'About Us Section'
        verbose_name_plural = 'About Us Sections'

    def __str__(self):
        return f"{self.get_section_type_display()}: {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class TeamMember(models.Model):
    section = models.ForeignKey(AboutUsSection, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = CKEditor5Field(config_name='extends')
    photo = models.ImageField(upload_to='team/')
    order = models.PositiveIntegerField(default=0)
    social_links = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.position}"

class ContactSubmission(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f"{self.name}  - {self.created_at.strftime('%Y-%m-%d')}"