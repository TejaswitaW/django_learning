# Generated by Django 3.0.6 on 2020-05-15 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='track',
            old_name='descritpiton',
            new_name='description',
        ),
    ]
