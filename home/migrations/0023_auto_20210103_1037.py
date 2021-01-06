# Generated by Django 3.1.4 on 2021-01-03 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_auto_20210102_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listfield',
            name='field_type',
            field=models.CharField(choices=[('text', 'Text'), ('long-text', 'Long Text'), ('number', 'Number')], default='text', max_length=250),
        ),
    ]