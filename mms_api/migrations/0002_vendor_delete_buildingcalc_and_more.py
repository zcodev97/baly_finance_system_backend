# Generated by Django 4.2.10 on 2024-03-05 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mms_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('vendor_id', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('cycle', models.CharField(max_length=255)),
                ('method', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=255)),
                ('fully_refunded', models.BooleanField()),
                ('penalized', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='BuildingCalc',
        ),
        migrations.RemoveField(
            model_name='company',
            name='company_type',
        ),
        migrations.RemoveField(
            model_name='company',
            name='container',
        ),
        migrations.RemoveField(
            model_name='company',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='company',
            name='supervisor',
        ),
        migrations.RemoveField(
            model_name='container',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='deposit',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='deposit',
            name='container',
        ),
        migrations.RemoveField(
            model_name='deposit',
            name='created_by',
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
        migrations.RemoveField(
            model_name='personal',
            name='container',
        ),
        migrations.RemoveField(
            model_name='personal',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='withdraw',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='withdraw',
            name='container',
        ),
        migrations.RemoveField(
            model_name='withdraw',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='withdraw',
            name='withdraw_type',
        ),
        migrations.DeleteModel(
            name='WorkerCalc',
        ),
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.DeleteModel(
            name='Container',
        ),
        migrations.DeleteModel(
            name='Deposit',
        ),
        migrations.DeleteModel(
            name='Personal',
        ),
        migrations.DeleteModel(
            name='Withdraw',
        ),
        migrations.DeleteModel(
            name='WithdrawType',
        ),
    ]
