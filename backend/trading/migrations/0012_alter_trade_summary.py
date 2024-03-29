# Generated by Django 4.1.6 on 2023-03-30 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0011_alter_trade_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='summary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trades', to='trading.summary'),
        ),
    ]
