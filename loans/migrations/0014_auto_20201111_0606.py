# Generated by Django 3.1.2 on 2020-11-11 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0013_loanscheduler_principal_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanrepayment',
            name='duration',
            field=models.CharField(blank=True, max_length=222, null=True),
        ),
        migrations.AddField(
            model_name='loanrepayment',
            name='interest',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=60, null=True),
        ),
    ]