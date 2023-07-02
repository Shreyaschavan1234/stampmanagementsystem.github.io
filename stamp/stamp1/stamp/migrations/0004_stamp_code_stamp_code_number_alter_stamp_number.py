# Generated by Django 4.1.2 on 2023-01-17 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stamp', '0003_alter_stamppurchase_series_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='stamp',
            name='code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='stamp',
            name='code_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='stamp',
            name='number',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
