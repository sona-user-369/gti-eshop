# Generated by Django 4.1.1 on 2022-11-21 12:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_remove_facture_date_livraison_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avis',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 21, 12, 41, 27, 723900, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='date_commande',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 21, 13, 41, 27, 718933)),
        ),
        migrations.AlterField(
            model_name='produit',
            name='date_de_stock',
            field=models.DateField(default=datetime.datetime(2022, 11, 21, 13, 41, 27, 718933)),
        ),
    ]
