# Generated by Django 4.2.10 on 2024-03-05 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mms_api', '0007_alter_payment_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='date_from',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date_to',
            field=models.DateTimeField(),
        ),
    ]
