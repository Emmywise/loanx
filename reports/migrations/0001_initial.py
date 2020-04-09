# Generated by Django 3.0.3 on 2020-04-08 19:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BranchCapital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_capital_date', models.DateField()),
                ('amount', models.PositiveIntegerField(default=0)),
                ('description', models.CharField(blank=True, max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CalendarEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=125)),
                ('date', models.DateTimeField()),
                ('till_date', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(blank=True, choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OtherIncome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('link_to_loan', models.URLField(blank=True, max_length=400, null=True)),
                ('is_recurring', models.BooleanField(default=False)),
                ('recurring', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='ProfitLoss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('operating_profit', models.CharField(blank=True, max_length=400, null=True)),
                ('interest_repayments', models.CharField(blank=True, max_length=400, null=True)),
                ('non_deductable_fees_repayments', models.CharField(blank=True, max_length=400, null=True)),
                ('deductable_fees_repayments', models.CharField(blank=True, max_length=400, null=True)),
                ('penalty_repayments', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_fees', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_commissions', models.CharField(blank=True, max_length=400, null=True)),
                ('operating_expenses', models.CharField(blank=True, max_length=400, null=True)),
                ('payroll', models.CharField(blank=True, max_length=400, null=True)),
                ('office_equipment', models.CharField(blank=True, max_length=400, null=True)),
                ('gross_profit', models.CharField(blank=True, max_length=400, null=True)),
                ('other_expenses', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_interest', models.CharField(blank=True, max_length=400, null=True)),
                ('default_loans', models.CharField(blank=True, max_length=400, null=True)),
                ('net_income', models.CharField(blank=True, max_length=400, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.Branch')),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Month')),
            ],
        ),
        migrations.CreateModel(
            name='OtherIncomeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='OtherIncomeDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='other_income')),
                ('other_income', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.OtherIncome')),
            ],
        ),
        migrations.AddField(
            model_name='otherincome',
            name='income_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.OtherIncomeType'),
        ),
        migrations.CreateModel(
            name='CustomOtherIncomeField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=125)),
                ('text_field', models.TextField(blank=True, null=True)),
                ('date_field', models.DateField(blank=True, null=True)),
                ('integer_field', models.PositiveIntegerField(blank=True, null=True)),
                ('decimal_field', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('url_field', models.URLField(blank=True, max_length=500, null=True)),
                ('text_area', models.TextField(blank=True, null=True)),
                ('dropdown_values', models.TextField(blank=True, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('dropdown', models.CharField(blank=True, max_length=200, null=True)),
                ('file_upload', models.FileField(blank=True, null=True, upload_to='other_income')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.OtherIncome')),
            ],
        ),
        migrations.CreateModel(
            name='CashFlowProjection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('operating_cash_beginning', models.CharField(blank=True, max_length=400, null=True)),
                ('branch_capital', models.CharField(blank=True, max_length=400, null=True)),
                ('principal_collections', models.CharField(blank=True, max_length=400, null=True)),
                ('interest_collections', models.CharField(blank=True, max_length=400, null=True)),
                ('fees_collections', models.CharField(blank=True, max_length=400, null=True)),
                ('penalty_collections', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_deposits', models.CharField(blank=True, max_length=400, null=True)),
                ('other_income', models.CharField(blank=True, max_length=400, null=True)),
                ('total_receipts', models.CharField(blank=True, max_length=400, null=True)),
                ('loan_disbursements', models.CharField(blank=True, max_length=400, null=True)),
                ('expenses', models.CharField(blank=True, max_length=400, null=True)),
                ('payroll', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_withdrawals', models.CharField(blank=True, max_length=400, null=True)),
                ('total_payments', models.CharField(blank=True, max_length=400, null=True)),
                ('total_cash_balance', models.CharField(blank=True, max_length=400, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.Branch')),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Month')),
            ],
        ),
        migrations.CreateModel(
            name='CashFlowMonthly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('opening_balance', models.CharField(blank=True, max_length=400, null=True)),
                ('loan_principal_repayments', models.CharField(blank=True, max_length=400, null=True)),
                ('loan_interest_repayments', models.CharField(blank=True, max_length=400, null=True)),
                ('loan_penalty_repayments', models.CharField(blank=True, max_length=400, null=True)),
                ('loan_fees_repayments', models.CharField(blank=True, max_length=400, null=True)),
                ('deductable_loan_fees', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_deposit', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_fees', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_commissions', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_transfer_in', models.CharField(blank=True, max_length=400, null=True)),
                ('other_income', models.CharField(blank=True, max_length=400, null=True)),
                ('total_receipts', models.CharField(blank=True, max_length=400, null=True)),
                ('expenses', models.CharField(blank=True, max_length=400, null=True)),
                ('payroll', models.CharField(blank=True, max_length=400, null=True)),
                ('loan_released', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_withdrawals', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_transfers_out', models.CharField(blank=True, max_length=400, null=True)),
                ('total_payments', models.CharField(blank=True, max_length=400, null=True)),
                ('total_cash_balance', models.CharField(blank=True, max_length=400, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.Branch')),
                ('branch_capital', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='reports.BranchCapital')),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Month')),
            ],
        ),
        migrations.CreateModel(
            name='CashFlowAccumulated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('loan_principal_repayment', models.CharField(blank=True, max_length=400, null=True)),
                ('loan_interest_repayment', models.CharField(blank=True, max_length=400, null=True)),
                ('loan_penalty_repayment', models.CharField(blank=True, max_length=400, null=True)),
                ('loan_fees_repayment', models.CharField(blank=True, max_length=400, null=True)),
                ('deductable_loan_fees', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_deposit', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_fees', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_commissions', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_transfer_in', models.CharField(blank=True, max_length=400, null=True)),
                ('other_income', models.CharField(blank=True, max_length=400, null=True)),
                ('total_receipts', models.CharField(blank=True, max_length=400, null=True)),
                ('expenses', models.CharField(blank=True, max_length=400, null=True)),
                ('payroll', models.CharField(blank=True, max_length=400, null=True)),
                ('loan_released', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_withdrawals', models.CharField(blank=True, max_length=400, null=True)),
                ('savings_transfers_out', models.CharField(blank=True, max_length=400, null=True)),
                ('total_payments', models.CharField(blank=True, max_length=400, null=True)),
                ('total_cash_balance', models.CharField(blank=True, max_length=400, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.Branch')),
                ('branch_capital', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='reports.BranchCapital')),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Month')),
            ],
        ),
        migrations.CreateModel(
            name='CalendarLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_type', models.CharField(choices=[('Disbursed', 'Disbursed'), ('Due Amount', 'Due Amount'), ('Maturity', 'Maturity'), ('Payment Schedule', 'Payment Schedule')], max_length=100)),
                ('url_path', models.CharField(max_length=400)),
                ('date', models.DateTimeField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Branch')),
            ],
            options={
                'get_latest_by': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='CalendarEventEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=225)),
                ('calendar_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.CalendarEvent')),
            ],
        ),
        migrations.CreateModel(
            name='BalanceSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('loans_outstanding', models.CharField(blank=True, max_length=400, null=True)),
                ('current', models.CharField(blank=True, max_length=400, null=True)),
                ('past_due', models.CharField(blank=True, max_length=400, null=True)),
                ('restructured', models.CharField(blank=True, max_length=400, null=True)),
                ('loan_loss_reserve', models.CharField(blank=True, max_length=400, null=True)),
                ('net_loans_outstanding', models.CharField(blank=True, max_length=400, null=True)),
                ('total_current_assets', models.CharField(blank=True, max_length=400, null=True)),
                ('total_investments', models.CharField(blank=True, max_length=400, null=True)),
                ('total_fixed_assets', models.CharField(blank=True, max_length=400, null=True)),
                ('brand', models.CharField(blank=True, max_length=400, null=True)),
                ('total_intangible_assets', models.CharField(blank=True, max_length=400, null=True)),
                ('total_other_assets', models.CharField(blank=True, max_length=400, null=True)),
                ('total_assets', models.CharField(blank=True, max_length=400, null=True)),
                ('client_savings', models.CharField(blank=True, max_length=400, null=True)),
                ('accounts_payable', models.CharField(blank=True, max_length=400, null=True)),
                ('wages_payable', models.CharField(blank=True, max_length=400, null=True)),
                ('short_term_borrowing', models.CharField(blank=True, max_length=400, null=True)),
                ('long_term_debt_commercial', models.CharField(blank=True, max_length=400, null=True)),
                ('long_term_debt_concessional', models.CharField(blank=True, max_length=400, null=True)),
                ('other_accrued_expenses_payable', models.CharField(blank=True, max_length=400, null=True)),
                ('income_taxes_payable', models.CharField(blank=True, max_length=400, null=True)),
                ('restricted_revenue', models.CharField(blank=True, max_length=400, null=True)),
                ('loan_fund_capital', models.CharField(blank=True, max_length=400, null=True)),
                ('retained_net_surplus', models.CharField(blank=True, max_length=400, null=True)),
                ('net_surplus', models.CharField(blank=True, max_length=400, null=True)),
                ('total_equity', models.CharField(blank=True, max_length=400, null=True)),
                ('total_liabilities_and_equity', models.CharField(blank=True, max_length=400, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.Branch')),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Month')),
            ],
        ),
    ]
