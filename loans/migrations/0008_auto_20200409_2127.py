# Generated by Django 3.0.3 on 2020-04-09 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0007_loanrepayment_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanrepayment',
            name='adjust_remaining_repayments',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='loanrepayment',
            name='charge_interest',
            field=models.CharField(blank=True, choices=[('normally', 'normally'), ('charge_on_release_date', 'charge_on_release_date'), ('charge_on_first_repayment', 'charge_on_first_repayment'), ('charge_on_last_repayment', 'charge_on_last_repayment'), ('do_not_charge_on_last_repayment', 'do_not_charge_on_last_repayment')], max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='loanrepayment',
            name='collector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='loans.LoanOfficer'),
        ),
        migrations.AlterField(
            model_name='loanrepayment',
            name='days_passed',
            field=models.PositiveIntegerField(blank=True, default=10, null=True),
        ),
        migrations.AlterField(
            model_name='loanrepayment',
            name='first_repayment_on_prorata',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='loanrepayment',
            name='grace_period',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='loanrepayment',
            name='grace_period_once_per_loan',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='loanrepayment',
            name='number_of_repayments',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='loanrepayment',
            name='penalty_branch_holiday',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='loanrepayment',
            name='status',
            field=models.CharField(blank=True, choices=[('accepted', 'accepted'), ('pending', 'pending'), ('declined', 'declined')], max_length=60, null=True),
        ),
    ]