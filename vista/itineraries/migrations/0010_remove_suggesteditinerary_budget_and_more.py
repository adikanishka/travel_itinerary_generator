# Generated by Django 5.1.7 on 2025-04-18 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itineraries', '0009_suggesteditinerary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suggesteditinerary',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='suggesteditinerary',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='suggesteditinerary',
            name='travel_mode',
        ),
    ]
