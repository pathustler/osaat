# Generated by Django 5.0.6 on 2024-07-02 10:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0013_technicianevent_confirmed_technicianevent_order_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="salesevent",
            name="address",
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="salesevent",
            name="appointment_notes",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="salesevent",
            name="main_phone",
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="GroupedJob",
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
                ("title", models.CharField(max_length=60)),
                ("done", models.BooleanField(default=False)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="delivery_jobs",
                        to="main.order",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DeliveryEvent",
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
                ("title", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=100)),
                ("special_instructions", models.TextField(blank=True, null=True)),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                (
                    "jobs",
                    models.ManyToManyField(
                        related_name="delivery_events", to="main.groupedjob"
                    ),
                ),
            ],
        ),
    ]
