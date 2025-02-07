# Generated by Django 5.1.4 on 2025-01-04 18:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_alter_customer_options_alter_address_city'),
        ('order', '0006_alter_order_options_alter_orderitem_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at'], 'verbose_name': 'Buyurtma', 'verbose_name_plural': 'Buyurtmalar'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['-created_at'], 'verbose_name': 'Buyurtma mahsuloti', 'verbose_name_plural': 'Buyurtma mahsulotlari'},
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Chegirma summasi'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='customer.address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='customer.customer'),
        ),
    ]
