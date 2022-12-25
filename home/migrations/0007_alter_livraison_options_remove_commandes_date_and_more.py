# Generated by Django 4.1.1 on 2022-11-02 18:55

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_favoris_id_alter_livraison_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='livraison',
            options={'verbose_name': 'Livraison'},
        ),
        migrations.RemoveField(
            model_name='commandes',
            name='date',
        ),
        migrations.RemoveField(
            model_name='commandes',
            name='lieu_livraison',
        ),
        migrations.RemoveField(
            model_name='livraison',
            name='date',
        ),
        migrations.RemoveField(
            model_name='livraison',
            name='livre',
        ),
        migrations.RemoveField(
            model_name='livraison',
            name='localisation',
        ),
        migrations.AddField(
            model_name='commandes',
            name='date_commande',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 2, 19, 55, 58, 102000)),
        ),
        migrations.AddField(
            model_name='commandes',
            name='date_livraison',
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name='livraison',
            name='address',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='livraison',
            name='city',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='livraison',
            name='first_name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='livraison',
            name='last_name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='livraison',
            name='phone_number',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='livree',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='produit',
            name='date_de_stock',
            field=models.DateField(default=datetime.datetime(2022, 11, 2, 19, 55, 58, 111777)),
        ),
    ]
