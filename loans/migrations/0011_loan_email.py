# Generated by Django 3.0.3 on 2020-04-10 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0010_auto_20200409_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='email',
            field=models.EmailField(blank=True, max_length=120, null=True),
        ),
    ]
