# Generated by Django 3.0 on 2020-05-08 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0020_auto_20200507_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanscheduler',
            name='due',
            field=models.FloatField(default=0, max_length=30),
        ),
        migrations.AddField(
            model_name='loanscheduler',
            name='fees',
            field=models.FloatField(default=0, max_length=30),
        ),
        migrations.AddField(
            model_name='loanscheduler',
            name='interest',
            field=models.FloatField(default=0, max_length=30),
        ),
        migrations.AddField(
            model_name='loanscheduler',
            name='paid',
            field=models.FloatField(default=0, max_length=30),
        ),
        migrations.AddField(
            model_name='loanscheduler',
            name='penalty',
            field=models.FloatField(default=0, max_length=30),
        ),
        migrations.AddField(
            model_name='loanscheduler',
            name='pending_due',
            field=models.FloatField(default=0, max_length=30),
        ),
        migrations.AddField(
            model_name='loanscheduler',
            name='principal',
            field=models.FloatField(default=0, max_length=30),
        ),
        migrations.AddField(
            model_name='loanscheduler',
            name='principal_due',
            field=models.FloatField(default=0, max_length=30),
        ),
        migrations.AddField(
            model_name='loanscheduler',
            name='total_due',
            field=models.FloatField(default=0, max_length=30),
        ),
    ]
