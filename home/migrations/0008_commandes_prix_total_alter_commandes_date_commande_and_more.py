# Generated by Django 4.1.1 on 2022-11-07 20:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_livraison_options_remove_commandes_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandes',
            name='prix_total',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='date_commande',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 7, 21, 12, 48, 482894)),
        ),
        migrations.AlterField(
            model_name='produit',
            name='date_de_stock',
            field=models.DateField(default=datetime.datetime(2022, 11, 7, 21, 12, 48, 482894)),
        ),
    ]
