# Generated by Django 3.1.4 on 2021-04-01 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ('author',), 'verbose_name': 'Follow list'},
        ),
    ]
