# Generated by Django 3.0 on 2020-05-07 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0019_auto_20200507_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='interest',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=100, null=True),
        ),
    ]
