# Generated by Django 5.0.6 on 2024-07-07 00:53

import main.storages
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0020_alter_technicianevent_appointment_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        storage=main.storages.WasabiStorage(), upload_to="documents/"
                    ),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="GalleryImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        storage=main.storages.WasabiStorage(), upload_to="gallery/"
                    ),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name="technicianevent",
            name="appointment_status",
            field=models.BooleanField(
                choices=[(0, "Inactive"), (1, "Active")], default=0
            ),
        ),
    ]
