# Generated by Django 4.1.1 on 2022-11-10 11:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_avis_date_alter_commandes_date_commande_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avis',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 10, 11, 16, 46, 917015, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='date_commande',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 10, 12, 16, 46, 912024)),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='date_livraison',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='produit',
            name='date_de_stock',
            field=models.DateField(default=datetime.datetime(2022, 11, 10, 12, 16, 46, 912024)),
        ),
    ]
