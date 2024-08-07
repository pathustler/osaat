# Generated by Django 5.0.6 on 2024-07-28 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0031_alter_technicianevent_appointment_notes_and_more"),
        ("workstation", "0002_tube_cut_job"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pre_Assembly_Job",
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
                ("job_complete", models.BooleanField(default=False)),
                ("tube", models.BooleanField(default=False)),
                ("box_end_caps", models.BooleanField(default=False)),
                ("track", models.BooleanField(default=False)),
                ("bottom_bar", models.BooleanField(default=False)),
                ("side_2_l_channels", models.BooleanField(default=False)),
                (
                    "unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pre_assembly_jobs",
                        to="main.unit",
                    ),
                ),
            ],
        ),
    ]
