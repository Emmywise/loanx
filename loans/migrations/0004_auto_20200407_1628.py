# Generated by Django 3.0.3 on 2020-04-07 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0003_loandisbursement_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='loandisbursement',
            name='duration',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='loandisbursement',
            name='loan_duration',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='loandisbursement',
            name='loan_duration_period',
            field=models.CharField(blank=True, choices=[('Days', 'Days'), ('Weeks', 'Weeks'), ('Months', 'Months'), ('Years', 'Years')], max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='loandisbursement',
            name='loan_interest_fixed_amount',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='loandisbursement',
            name='loan_interest_percentage',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='loandisbursement',
            name='loan_interest_percentage_period',
            field=models.CharField(blank=True, choices=[('Days', 'Days'), ('Weeks', 'Weeks'), ('Months', 'Months'), ('Years', 'Years')], max_length=400, null=True),
        ),
    ]
