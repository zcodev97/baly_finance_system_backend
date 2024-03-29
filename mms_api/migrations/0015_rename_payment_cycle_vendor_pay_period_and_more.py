# Generated by Django 4.2.9 on 2024-03-12 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mms_api', '0014_alter_payment_vendor_id_alter_payment_vendor_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor',
            old_name='payment_cycle',
            new_name='pay_period',
        ),
        migrations.RenameField(
            model_name='vendor',
            old_name='payment_method',
            new_name='pay_type',
        ),
        migrations.AddField(
            model_name='vendor',
            name='owner_name',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendor',
            name='owner_phone',
            field=models.CharField(default='teasdasd', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vendor',
            name='number',
            field=models.IntegerField(blank=True),
        ),
    ]
