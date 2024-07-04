# Generated by Django 5.0.6 on 2024-07-02 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0015_alter_crew_crew_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="technicianevent",
            name="crew",
            field=models.CharField(
                choices=[("c1", "Crew 1"), ("c2", "Crew 2"), ("c3", "Crew 3")],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="technicianevent",
            name="status",
            field=models.CharField(
                choices=[
                    ("active", "Active"),
                    ("estimate", "Estimate"),
                    ("sold", "Sold"),
                    ("cancelled", "Cancelled"),
                ],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="technicianevent",
            name="visit_type",
            field=models.CharField(
                choices=[
                    ("installation", "Installation"),
                    ("warranty", "Warranty Serice"),
                    ("tech", "Tech Measure"),
                    ("service", "Service"),
                ],
                max_length=100,
            ),
        ),
    ]