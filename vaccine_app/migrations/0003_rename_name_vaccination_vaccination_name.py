# Generated by Django 5.2 on 2025-04-21 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine_app', '0002_rename_notes_appointment_appointment_notes_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vaccination',
            old_name='name',
            new_name='vaccination_name',
        ),
    ]
