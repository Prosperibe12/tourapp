# Generated by Django 4.0.6 on 2022-07-22 14:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0004_alter_tour_arrival_alter_tour_departure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='arrival',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='tour',
            name='departure',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
