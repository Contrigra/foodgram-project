# Generated by Django 3.1.4 on 2021-04-01 22:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210329_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='time',
            field=models.PositiveSmallIntegerField(default=10, help_text='Укажите время в минутах', validators=[django.core.validators.MinValueValidator(1, message='Время должно быть равно 1 или более минут')]),
        ),
    ]