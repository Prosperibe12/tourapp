# Generated by Django 4.0.6 on 2022-07-21 15:38

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0002_alter_tour_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='package',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Air Fares', 'Air Fares'), ('4 Nights Hotel Accomodation', '4 Nights Hotel Accomodation'), ('Entrance Fee', 'Entrance Fee'), ('Tour Guide', 'Tour Guide')], max_length=200, null=True),
        ),
    ]
