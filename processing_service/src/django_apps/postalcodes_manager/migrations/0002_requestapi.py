# Generated by Django 5.0.4 on 2024-04-15 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("postalcodes_manager", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RequestApi",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("url", models.CharField(max_length=255)),
                ("response", models.JSONField()),
            ],
            options={
                "db_table": "request_api",
            },
        ),
    ]
