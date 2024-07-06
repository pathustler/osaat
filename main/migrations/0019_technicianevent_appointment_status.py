# Generated by Django 5.0.6 on 2024-07-05 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0018_rename_title_technicianevent_address_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="technicianevent",
            name="appointment_status",
            field=models.BooleanField(
                choices=[(1, "Active"), (0, "Inactive")], default=0
            ),
            preserve_default=False,
        ),
    ]