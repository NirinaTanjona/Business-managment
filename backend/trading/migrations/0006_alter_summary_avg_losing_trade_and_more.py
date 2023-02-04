# Generated by Django 4.1.6 on 2023-02-04 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0005_summary_avg_losing_trade_summary_avg_winning_trade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='avg_losing_trade',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='summary',
            name='avg_winning_trade',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='summary',
            name='largest_losing_trade',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='summary',
            name='largest_winning_trade',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='summary',
            name='total_trade_costs',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='trade',
            name='closed_position',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]