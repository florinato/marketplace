# Generated by Django 5.1.3 on 2024-12-02 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_remove_product_is_active_product_is_blocked_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_reserved',
        ),
    ]