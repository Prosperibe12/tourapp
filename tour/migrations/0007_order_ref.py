# Generated by Django 4.0.6 on 2022-07-28 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0006_cart_order_cartproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ref',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]