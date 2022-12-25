# Generated by Django 4.1.1 on 2022-10-21 03:08

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_panier_id_alter_produit_date_de_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoris',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='date',
            field=models.DateField(default=datetime.date(2022, 10, 21)),
        ),
        migrations.AlterField(
            model_name='produit',
            name='date_de_stock',
            field=models.DateField(default=datetime.datetime(2022, 10, 21, 4, 8, 54, 189260)),
        ),
    ]
