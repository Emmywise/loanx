# Generated by Django 3.1.2 on 2020-11-10 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='is_open',
            field=models.BooleanField(default=False),
        ),
    ]