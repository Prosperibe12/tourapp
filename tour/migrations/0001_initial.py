# Generated by Django 4.0.6 on 2022-07-19 11:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='banners')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('destination', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('age_range', models.IntegerField()),
                ('price', models.IntegerField()),
                ('main_photo', models.ImageField(upload_to='photos')),
                ('photo1', models.ImageField(upload_to='photos')),
                ('photo2', models.ImageField(upload_to='photos')),
                ('photo3', models.ImageField(upload_to='photos')),
                ('refund_policy', models.CharField(max_length=100)),
                ('package', models.CharField(choices=[('Air Fares', 'Air Fares'), ('4 Nights Hotel Accomodation', '4 Nights Hotel Accomodation'), ('Entrance Fee', 'Entrance Fee'), ('Tour Guide', 'Tour Guide')], max_length=200)),
                ('departure', models.DateTimeField(auto_now_add=True)),
                ('arrival', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]