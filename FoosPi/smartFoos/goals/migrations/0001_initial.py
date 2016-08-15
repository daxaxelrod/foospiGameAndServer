# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-15 14:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winner', models.CharField(choices=[('Red', 'Red Won'), ('Blue', 'Blue Won')], max_length=4)),
                ('final_score', models.CharField(max_length=20)),
                ('epic_goal', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('duration', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('path_to_sound_file', models.CharField(max_length=255, unique=True)),
                ('wins', models.IntegerField(default=0)),
                ('losses', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='blue_player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blue_player', to='goals.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='red_player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='red_player', to='goals.Player'),
        ),
    ]
