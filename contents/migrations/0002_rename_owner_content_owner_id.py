# Generated by Django 3.2.4 on 2021-08-04 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='owner',
            new_name='owner_id',
        ),
    ]
