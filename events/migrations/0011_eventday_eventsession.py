# Generated by Django 5.1.5 on 2025-01-26 01:32

import django.db.models.deletion
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_speaker_address_speaker_banner_photo_speaker_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('title', models.CharField(blank=True, max_length=200)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='days', to='events.event')),
            ],
            options={
                'ordering': ['date'],
                'unique_together': {('event', 'date')},
            },
        ),
        migrations.CreateModel(
            name='EventSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('title', models.CharField(max_length=200)),
                ('description', django_ckeditor_5.fields.CKEditor5Field()),
                ('session_type', models.CharField(choices=[('PRESENTATION', 'Presentation'), ('BREAK', 'Break'), ('QA', 'Q&A Session'), ('WORKSHOP', 'Workshop'), ('NETWORKING', 'Networking')], default='PRESENTATION', max_length=20)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='events.eventday')),
                ('speakers', models.ManyToManyField(blank=True, to='events.speaker')),
            ],
            options={
                'ordering': ['start_time'],
            },
        ),
    ]
