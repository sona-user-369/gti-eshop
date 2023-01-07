# Generated by Django 4.1.1 on 2022-12-23 17:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_contact_create_at_alter_avis_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avis',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 23, 17, 9, 59, 507079, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='date_commande',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 23, 17, 9, 59, 491457, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='contact',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 23, 17, 9, 59, 507079, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='produit',
            name='date_de_stock',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 23, 17, 9, 59, 491457, tzinfo=datetime.timezone.utc)),
        ),
    ]