# Generated by Django 3.1.4 on 2020-12-17 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20201217_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.organization'),
        ),
    ]
