# Generated by Django 3.1.2 on 2020-11-06 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0003_auto_20201106_2227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanguarantor',
            name='country',
        ),
    ]