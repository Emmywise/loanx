# Generated by Django 3.1.2 on 2020-11-10 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_branch_is_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='remaining_capital',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=100),
        ),
        migrations.AddField(
            model_name='branch',
            name='spent_capital',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=100),
        ),
    ]