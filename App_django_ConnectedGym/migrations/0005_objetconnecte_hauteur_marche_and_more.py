# Generated by Django 5.1.7 on 2025-04-30 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("App_django_ConnectedGym", "0004_objetconnecte_amorti_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="objetconnecte",
            name="hauteur_marche",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=5, null=True
            ),
        ),
        migrations.AddField(
            model_name="objetconnecte",
            name="longueur_pas",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=5, null=True
            ),
        ),
        migrations.AddField(
            model_name="objetconnecte",
            name="longueur_rail",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=5, null=True
            ),
        ),
        migrations.AddField(
            model_name="objetconnecte",
            name="type_mouvement",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
