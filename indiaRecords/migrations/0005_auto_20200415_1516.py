# Generated by Django 3.0.4 on 2020-04-15 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indiaRecords', '0004_auto_20200415_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmedtimeseriesstate',
            name='date',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='deathstimeseriesstate',
            name='date',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='indiatimeseries',
            name='date',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='recoveredtimeseriesstate',
            name='date',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
