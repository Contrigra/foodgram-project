# Generated by Django 3.1.4 on 2021-03-28 21:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210327_0258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='time',
            field=models.PositiveSmallIntegerField(default=10, help_text='Укажите время в минутах', validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
