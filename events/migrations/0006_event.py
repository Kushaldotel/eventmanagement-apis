# Generated by Django 5.1.5 on 2025-01-25 06:18

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Description')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('location', models.TextField()),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('featured', models.BooleanField(default=False)),
                ('featured_image', models.ImageField(upload_to='events/featured/')),
                ('registration_deadline', models.DateTimeField()),
                ('max_participants', models.PositiveIntegerField()),
                ('registration_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('event_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_registration_open', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categories', models.ManyToManyField(to='events.category')),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
    ]
