# Generated by Django 5.1.5 on 2025-01-30 08:02

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_policydocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralFAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', django_ckeditor_5.fields.CKEditor5Field()),
                ('category', models.CharField(blank=True, max_length=100)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'General FAQ',
                'verbose_name_plural': 'General FAQs',
                'ordering': ['order'],
            },
        ),
        migrations.AlterField(
            model_name='policydocument',
            name='document_type',
            field=models.CharField(choices=[('PRIVACY', 'Privacy Policy'), ('TERMS', 'Terms & Conditions'), ('DISCLAIMER', 'Disclaimer'), ('PAYMENT', 'Payment Policy'), ('COOKIES', 'Cookies Policy'), ('REFUND', 'Refund Policy'), ('CODE_OF_CONDUCT', 'Code of Conduct'), ('SOCIA_MEDIA_MARKEING_POLICY', 'Social Media Marketing Policy'), ('INSURANCE_POLICY', 'Insurance Policy'), ('HEALTH_SAFETY_POLICY', 'Health & Safety Policy')], max_length=40, unique=True),
        ),
    ]
