# Generated by Django 5.1.4 on 2025-01-02 14:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Kategoriya nomi')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Kategoriya tavsifi')),
                ('image', models.ImageField(blank=True, null=True, upload_to='Categories/', verbose_name='Rasmi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'category',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='nomi')),
                ('description', models.TextField(blank=True, null=True, verbose_name='hususiyatlari')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='narxi')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='soni')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='rasmi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category')),
            ],
            options={
                'verbose_name': 'Mahsulot',
                'verbose_name_plural': 'Mahsulotlar',
                'db_table': 'product',
                'ordering': ['-created_at'],
            },
        ),
    ]
