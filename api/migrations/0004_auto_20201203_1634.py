# Generated by Django 3.0.5 on 2020-12-03 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20201202_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='dimension',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Dimension'),
        ),
    ]