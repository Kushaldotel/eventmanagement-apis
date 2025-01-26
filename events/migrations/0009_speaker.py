# Generated by Django 5.1.5 on 2025-01-26 00:23

import django.db.models.deletion
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bio', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Bio')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='speakers/')),
                ('designation', models.CharField(max_length=100)),
                ('organization', models.CharField(blank=True, max_length=100)),
                ('socials', models.JSONField(blank=True, null=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speakers', to='events.event')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
