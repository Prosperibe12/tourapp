# Generated by Django 4.0.6 on 2022-07-19 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]