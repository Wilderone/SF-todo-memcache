# Generated by Django 3.0.8 on 2020-07-21 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_auto_20200721_0148'),
    ]

    operations = [
        migrations.RenameField(
            model_name='priorchoice',
            old_name='high',
            new_name='priority',
        ),
        migrations.RemoveField(
            model_name='priorchoice',
            name='low',
        ),
        migrations.RemoveField(
            model_name='priorchoice',
            name='medium',
        ),
    ]