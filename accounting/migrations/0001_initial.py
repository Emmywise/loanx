# Generated by Django 3.1.2 on 2021-01-08 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfitLoss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_capital', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now=True)),
                ('interest_repayment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('non_deductable_fees_repayment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('deductable_fees_repayment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('penalty_repayment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('savings_fees', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('savings_commissions', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('investor_account_fees', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('investor_account_commissions', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('payroll', models.DecimalField(decimal_places=2, max_digits=10)),
                ('savings_interest', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('investor_acct_interest', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('default_loans', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profit_loss_branch', to='accounts.branch')),
            ],
        ),
        migrations.CreateModel(
            name='CashFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_capital', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now=True)),
                ('loan_principal_repayments', models.DecimalField(decimal_places=2, max_digits=10)),
                ('loan_interest_repayments', models.DecimalField(decimal_places=2, max_digits=10)),
                ('loan_penalty_repayments', models.DecimalField(decimal_places=2, max_digits=10)),
                ('loan_fees_repayments', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deductable_loan_fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('savings_deposits', models.DecimalField(decimal_places=2, max_digits=10)),
                ('savings_fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('savings_commissions', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('savings_transfer_in', models.DecimalField(decimal_places=2, max_digits=10)),
                ('investor_account_deposits', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('investor_account_fees', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('investor_account_commissions', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('investor_account_transfer_in', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('other_income', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('expenses', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payroll', models.DecimalField(decimal_places=2, max_digits=10)),
                ('loan_released', models.DecimalField(decimal_places=2, max_digits=10)),
                ('savings_withdrawals', models.DecimalField(decimal_places=2, max_digits=10)),
                ('savings_transfer_out', models.DecimalField(decimal_places=2, max_digits=10)),
                ('investor_account_withdrawals', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('investor_account_transfer_out', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cash_flow_branch', to='accounts.branch')),
            ],
        ),
        migrations.CreateModel(
            name='BalanceSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_capital', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now=True)),
                ('current', models.DecimalField(decimal_places=2, max_digits=10)),
                ('past_due', models.DecimalField(decimal_places=2, max_digits=10)),
                ('restructured', models.DecimalField(decimal_places=2, max_digits=10)),
                ('loan_loss_reserve', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_investments', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_fixed_assets', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_intangible_assets', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_other_assets', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('client_savings', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('account_payable', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('wages_payable', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('short_term_borrowing', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('long_term_debt_commercial_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('long_term_debt_concessional_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('other_accrued_expenses', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('income_taxes_payable', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('restricted_revenue', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('loan_fund_capital', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('retained_net_surplus', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('net_surplus', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='balance_sheet_branch', to='accounts.branch')),
            ],
        ),
    ]
