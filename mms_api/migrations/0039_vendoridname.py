# Generated by Django 4.2.9 on 2024-04-17 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mms_api', '0038_vendor_commission_after_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorIDName',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('arName', models.CharField(max_length=255)),
                ('enName', models.CharField(max_length=255)),
            ],
        ),
    ]