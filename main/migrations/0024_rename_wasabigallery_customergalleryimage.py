# Generated by Django 5.0.6 on 2024-07-08 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0023_alter_technicianevent_visit_type"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="WasabiGallery",
            new_name="CustomerGalleryImage",
        ),
    ]
