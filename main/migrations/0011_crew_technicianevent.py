# Generated by Django 5.0.6 on 2024-07-01 10:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0010_order_confirmed"),
    ]

    operations = [
        migrations.CreateModel(
            name="Crew",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="TechnicianEvent",
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
                ("technician", models.CharField(max_length=100)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Active", "active"),
                            ("Estimate", "estimate"),
                            ("Sold", "sold"),
                            ("Cancelled", "cancelled"),
                        ],
                        max_length=100,
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                (
                    "crew",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.crew"
                    ),
                ),
            ],
        ),
    ]
