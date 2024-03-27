# Generated by Django 4.2.9 on 2024-03-25 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mms_api', '0024_payment_orders_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_cycle',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='payment',
            name='vendor_id',
            field=models.IntegerField(unique=True),
        ),
    ]
