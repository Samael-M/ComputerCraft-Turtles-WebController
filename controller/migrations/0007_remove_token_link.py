# Generated by Django 4.2.3 on 2024-03-05 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("controller", "0006_token_link"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="token",
            name="link",
        ),
    ]
