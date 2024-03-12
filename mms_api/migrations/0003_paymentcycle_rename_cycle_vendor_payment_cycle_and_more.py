# Generated by Django 4.2.10 on 2024-03-05 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mms_api', '0002_vendor_delete_buildingcalc_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentCycle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameField(
            model_name='vendor',
            old_name='cycle',
            new_name='payment_cycle',
        ),
        migrations.RenameField(
            model_name='vendor',
            old_name='method',
            new_name='payment_method',
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('vendor_id', models.CharField(max_length=255, unique=True)),
                ('date_from', models.CharField(max_length=255, unique=True)),
                ('date_to', models.CharField(max_length=255)),
                ('payment_cycle', models.CharField(max_length=255)),
                ('payment_method', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=255)),
                ('amount', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaidOrders',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('payment_id', models.CharField(max_length=255, unique=True)),
                ('order_id', models.CharField(max_length=255, unique=True)),
                ('amount', models.CharField(max_length=255)),
                ('paid', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
