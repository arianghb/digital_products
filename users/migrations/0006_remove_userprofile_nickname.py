# Generated by Django 4.2.7 on 2023-11-07 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_userprofile_nickname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='nickname',
        ),
    ]
