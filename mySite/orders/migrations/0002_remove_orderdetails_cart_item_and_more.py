# Generated by Django 5.1.1 on 2024-11-28 12:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetails',
            name='cart_item',
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='order_item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.product'),
            preserve_default=False,
        ),
    ]
