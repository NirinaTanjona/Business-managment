# Generated by Django 4.1.6 on 2023-02-06 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0021_rename_average_risk_reward_per_trade_summary_average_risk_reward'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='actual_exit_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='trade',
            name='discipline_rating',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trade',
            name='emotional_state_of_mind',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trade',
            name='screen_after',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trade',
            name='screen_before',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trade',
            name='trade_notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trade',
            name='entry_price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='trade',
            name='stop_loss_price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='trade',
            name='take_profit_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
