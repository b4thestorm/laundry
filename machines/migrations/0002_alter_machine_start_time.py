# Generated by Django 3.2.3 on 2021-05-30 03:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 30, 3, 59, 9, 943217)),
        ),
    ]
