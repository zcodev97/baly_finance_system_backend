# Generated by Django 4.2.9 on 2024-04-04 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mms_api', '0028_vendor_owner_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='log',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]