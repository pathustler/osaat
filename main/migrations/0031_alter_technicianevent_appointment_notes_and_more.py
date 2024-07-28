# Generated by Django 5.0.6 on 2024-07-15 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0030_alter_job_status_alter_salesevent_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="technicianevent",
            name="appointment_notes",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="technicianevent",
            name="crew",
            field=models.CharField(
                blank=True,
                choices=[
                    ("c1", "Crew 1"),
                    ("c2", "Crew 2"),
                    ("c3", "Crew 3"),
                    ("unset", "Unset"),
                ],
                default="unset",
                max_length=20,
                null=True,
            ),
        ),
    ]