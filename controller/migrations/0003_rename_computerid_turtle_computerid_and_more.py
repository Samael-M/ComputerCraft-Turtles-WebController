# Generated by Django 4.2.3 on 2024-03-04 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("controller", "0002_turtle_computerid_turtle_worldid"),
    ]

    operations = [
        migrations.RenameField(
            model_name="turtle",
            old_name="ComputerID",
            new_name="computerID",
        ),
        migrations.AlterField(
            model_name="turtle",
            name="worldID",
            field=models.IntegerField(default=0),
        ),
    ]