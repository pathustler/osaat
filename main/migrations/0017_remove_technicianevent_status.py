# Generated by Django 5.0.6 on 2024-07-02 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0016_alter_technicianevent_crew_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="technicianevent",
            name="status",
        ),
    ]