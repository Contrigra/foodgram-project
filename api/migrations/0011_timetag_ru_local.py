# Generated by Django 3.1.4 on 2021-03-09 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20210309_0159'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetag',
            name='ru_local',
            field=models.CharField(default='local', max_length=64),
            preserve_default=False,
        ),
    ]
