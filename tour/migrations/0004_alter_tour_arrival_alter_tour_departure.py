# Generated by Django 4.0.6 on 2022-07-21 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0003_alter_tour_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='arrival',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='tour',
            name='departure',
            field=models.DateTimeField(),
        ),
    ]