# Generated by Django 5.0.6 on 2024-06-21 05:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_timeline_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                ("account_name", models.CharField(max_length=255)),
                ("po_number", models.CharField(max_length=100)),
                ("ship_to", models.CharField(max_length=255)),
                ("shipping_address", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=50)),
                ("zip_code", models.CharField(max_length=20)),
                ("phone", models.CharField(max_length=20)),
                ("ship_via", models.CharField(max_length=100)),
                (
                    "installation_address_same_as_shipping",
                    models.BooleanField(default=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Unit",
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
                ("unit_count", models.IntegerField()),
                ("manual_shade", models.BooleanField(default=False)),
                (
                    "product_type_manual",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "width_manual",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "drop_manual",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "handing_manual",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "box_color_manual",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "fabric_color_manual",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "mounting_manual",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "product_type_motorized",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "width_motorized",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "drop_motorized",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "handing_motorized",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("motor_type", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "remote_type",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "box_color_motorized",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "fabric_type_motorized",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "fabric_color_motorized",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "mounting_motorized",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "hardware_color_motorized",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "cable_mount_motorized",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "cable_size_motorized",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="units",
                        to="main.order",
                    ),
                ),
            ],
        ),
    ]