# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-11 16:25
from __future__ import unicode_literals
from django.db import migrations
from django.core.management import call_command


def load_fixture(apps, schema_editor):
    # call_command('loaddata', 'initial_data', app_label='users')
    pass


def unload_fixture(apps, schema_editor):
    # model = apps.get_model("users", "User")
    # model.objects.all().delete()
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    # operations = [
    #     migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    # ]
