# Generated by Django 4.1.1 on 2022-11-28 15:53

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_produit_qr_code_file_alter_avis_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avis',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 28, 15, 53, 12, 308566, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='date_commande',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 28, 16, 53, 12, 299030)),
        ),
        migrations.AlterField(
            model_name='produit',
            name='date_de_stock',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 28, 16, 53, 12, 299030)),
        ),
        migrations.AlterField(
            model_name='produit',
            name='sous_categorie',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.souscategorie'),
        ),
    ]
