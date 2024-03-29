# Generated by Django 3.1.4 on 2021-03-17 22:45

import django.core.validators
import django.db.models.deletion
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('units', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, unique=True)),
                ('image', models.ImageField(blank=True, null=True,
                                            upload_to='recipes')),
                ('time',
                 models.PositiveSmallIntegerField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=256, unique=True)),
                ('pub_date',
                 models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='date published')),
                ('description', models.TextField()),
                ('author',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='recipes',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='TimeTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True,
                                          verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True,
                                          verbose_name='slug')),
                ('colour', models.CharField(max_length=256)),
                ('ru_local', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'TimeTags',
            },
        ),
        migrations.CreateModel(
            name='Shoplist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('recipes',
                 models.ManyToManyField(blank=True, to='api.Recipe')),
                ('user', models.OneToOneField(blank=True, null=True,
                                              on_delete=django.db.models.deletion.CASCADE,
                                              to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Shopping List',
                'verbose_name_plural': 'Shopping Lists',
            },
        ),
        migrations.CreateModel(
            name='RecipeTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('object_id',
                 models.IntegerField(db_index=True, verbose_name='object ID')),
                ('content_type',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='api_recipetag_tagged_items',
                                   to='contenttypes.contenttype',
                                   verbose_name='content type')),
                ('tag',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='api_recipetag_items',
                                   to='api.timetag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('value', models.PositiveSmallIntegerField(default=10,
                                                           help_text='Добавьте необходимое количество ингредиентов',
                                                           validators=[
                                                               django.core.validators.MinValueValidator(
                                                                   1)],
                                                           verbose_name='ingredient weight')),
                ('ingredient', models.ForeignKey(null=True,
                                                 on_delete=django.db.models.deletion.SET_NULL,
                                                 to='api.ingredient')),
                ('recipe',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='api.recipe')),
            ],
            options={
                'verbose_name': 'Recipe Ingredient',
                'verbose_name_plural': 'Recipe Ingredients',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True,
                                         related_name='ingredients',
                                         through='api.RecipeIngredient',
                                         to='api.Ingredient',
                                         verbose_name='Ингредиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=taggit.managers.TaggableManager(
                help_text='A comma-separated list of tags.',
                through='api.RecipeTag', to='api.TimeTag',
                verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('recipes',
                 models.ManyToManyField(blank=True, to='api.Recipe')),
                ('user', models.OneToOneField(blank=True, null=True,
                                              on_delete=django.db.models.deletion.CASCADE,
                                              to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Favorite list',
                'verbose_name_plural': 'Favorite lists',
            },
        ),
    ]
