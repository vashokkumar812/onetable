# Generated by Django 3.1.4 on 2020-12-19 19:55

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='fields',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
    ]