# Generated by Django 4.2.9 on 2024-03-17 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mms_api', '0022_alter_payment_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='vendor_name',
            new_name='vendor',
        ),
    ]