# Generated by Django 4.2.9 on 2024-03-17 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mms_api', '0018_alter_paidorders_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='is_paid',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
