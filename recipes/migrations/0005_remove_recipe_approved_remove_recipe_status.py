# Generated by Django 4.2.11 on 2024-04-15 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0004_rating"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recipe",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="recipe",
            name="status",
        ),
    ]
