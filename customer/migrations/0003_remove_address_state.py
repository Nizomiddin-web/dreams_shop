# Generated by Django 5.1.4 on 2025-01-08 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_alter_customer_options_alter_address_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='state',
        ),
    ]
