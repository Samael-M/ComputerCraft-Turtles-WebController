# Generated by Django 4.2.3 on 2024-03-05 02:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("controller", "0003_rename_computerid_turtle_computerid_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Token",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("date", models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name="turtle",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterUniqueTogether(
            name="turtle",
            unique_together={("computerID", "worldID")},
        ),
    ]