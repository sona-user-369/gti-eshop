# Generated by Django 4.1.1 on 2022-11-08 13:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_avis_name_avis_rating_alter_avis_contenu_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avis',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 11, 8, 14, 23, 9, 717552)),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='date_commande',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 8, 14, 23, 9, 698490)),
        ),
        migrations.AlterField(
            model_name='produit',
            name='date_de_stock',
            field=models.DateField(default=datetime.datetime(2022, 11, 8, 14, 23, 9, 709526)),
        ),
    ]
