# Generated by Django 4.1.1 on 2022-12-12 01:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_contact_alter_avis_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avis',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 12, 1, 15, 20, 377602, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='date_commande',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 12, 1, 15, 20, 371598, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='produit',
            name='date_de_stock',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 12, 1, 15, 20, 373600, tzinfo=datetime.timezone.utc)),
        ),
    ]