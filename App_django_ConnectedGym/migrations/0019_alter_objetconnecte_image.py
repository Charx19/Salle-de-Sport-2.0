# Generated by Django 5.1.7 on 2025-05-03 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("App_django_ConnectedGym", "0018_alter_objetconnecte_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="objetconnecte",
            name="image",
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
    ]
