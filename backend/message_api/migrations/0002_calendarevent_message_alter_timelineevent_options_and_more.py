# Generated by Django 5.2.1 on 2025-06-02 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("message_api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CalendarEvent",
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
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True, null=True)),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField(blank=True, null=True)),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("holiday", "Holiday"),
                            ("memo", "Memo"),
                            ("log", "Log"),
                            ("other", "Other"),
                        ],
                        default="memo",
                        max_length=20,
                    ),
                ),
                ("is_all_day", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["start_time"],
            },
        ),
        migrations.CreateModel(
            name="Message",
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
                ("content", models.TextField()),
                (
                    "author",
                    models.CharField(blank=True, default="Anonymous", max_length=100),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name="timelineevent",
            options={"ordering": ["-date", "-created_at"]},
        ),
        migrations.AlterField(
            model_name="timelineevent",
            name="title",
            field=models.CharField(max_length=200),
        ),
    ]
