# Generated by Django 3.2 on 2023-06-14 18:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0004_auto_20230614_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.IntegerField(blank=True, default=0, validators=[django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(blank=True, default=2023, validators=[django.core.validators.MaxValueValidator(2023)]),
        ),
    ]
