# Generated by Django 3.2.4 on 2021-08-04 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('owners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=300)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(blank=True, max_length=40, null=True)),
                ('pub_date', models.CharField(blank=True, max_length=50, null=True)),
                ('img_url', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('owner', models.ForeignKey(db_column='owner_id', on_delete=django.db.models.deletion.CASCADE, to='owners.owner')),
            ],
        ),
    ]
