# Generated by Django 4.1.1 on 2022-11-16 17:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_categorie_image_commandes_valide_alter_avis_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandes',
            name='pending',
            field=models.BooleanField(default=1),
        ),
        migrations.AlterField(
            model_name='avis',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 16, 17, 22, 19, 622356, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='date_commande',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 16, 18, 22, 19, 622356)),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='valide',
            field=models.BooleanField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='produit',
            name='date_de_stock',
            field=models.DateField(default=datetime.datetime(2022, 11, 16, 18, 22, 19, 622356)),
        ),
    ]
