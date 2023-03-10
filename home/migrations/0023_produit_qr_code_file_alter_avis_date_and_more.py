# Generated by Django 4.1.1 on 2022-11-28 14:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_alter_avis_date_alter_commandes_date_commande_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='qr_code_file',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='avis',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 28, 14, 12, 8, 807477, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='date_commande',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 28, 15, 12, 8, 802478)),
        ),
        migrations.AlterField(
            model_name='facture',
            name='source',
            field=models.FileField(null=True, upload_to='invoices'),
        ),
        migrations.AlterField(
            model_name='produit',
            name='date_de_stock',
            field=models.DateField(default=datetime.datetime(2022, 11, 28, 15, 12, 8, 802478)),
        ),
    ]
