# Generated by Django 4.1.6 on 2023-03-30 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0010_summary_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='summary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trading.summary'),
        ),
    ]