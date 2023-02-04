# Generated by Django 4.1.6 on 2023-02-03 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='total_number_of_trades',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='summary',
            name='total_number_of_winning_trades',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
