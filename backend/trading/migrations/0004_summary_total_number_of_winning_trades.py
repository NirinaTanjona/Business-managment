# Generated by Django 4.1.6 on 2023-02-04 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0003_remove_summary_total_number_of_winning_trades_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='total_number_of_winning_trades',
            field=models.PositiveIntegerField(default=0),
        ),
    ]