# Generated by Django 5.1.7 on 2025-04-22 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itineraries', '0012_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='submitted_at',
        ),
        migrations.AlterField(
            model_name='feedback',
            name='rating',
            field=models.IntegerField(),
        ),
    ]
