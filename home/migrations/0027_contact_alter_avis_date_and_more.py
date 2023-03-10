# Generated by Django 4.1.1 on 2022-12-10 21:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_produit_is_archive_alter_avis_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Contacts',
            },
        ),
        migrations.AlterField(
            model_name='avis',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 10, 21, 44, 21, 382785, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='date_commande',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 10, 21, 44, 21, 375787, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='produit',
            name='date_de_stock',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 10, 21, 44, 21, 377785, tzinfo=datetime.timezone.utc)),
        ),
    ]
