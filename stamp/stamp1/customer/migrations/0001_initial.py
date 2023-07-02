# Generated by Django 4.1.2 on 2023-01-15 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('aadhaar', models.CharField(blank=True, max_length=10, null=True)),
                ('mobile', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('tehsil', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=100)),
                ('pincode', models.IntegerField()),
            ],
            options={
                'db_table': 'customers',
            },
        ),
    ]
