# Generated by Django 3.0.3 on 2020-05-06 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_branch_capital'),
        ('accounting', '0004_auto_20200504_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashflow',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cash_flow_branch', to='accounts.Branch'),
        ),
        migrations.CreateModel(
            name='ProfitLoss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_capital', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now=True)),
                ('interest_repayment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('non_deductable_fees_repayment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deductable_fees_repayment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('penalty_repayment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('savings_fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('savings_commissions', models.DecimalField(decimal_places=2, max_digits=10)),
                ('investor_account_fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('investor_account_commissions', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payroll', models.DecimalField(decimal_places=2, max_digits=10)),
                ('savings_interest', models.DecimalField(decimal_places=2, max_digits=10)),
                ('investor_acct_interest', models.DecimalField(decimal_places=2, max_digits=10)),
                ('default_loans', models.DecimalField(decimal_places=2, max_digits=10)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profit_loss_branch', to='accounts.Branch')),
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
                ('loan_loss_reserve', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_investments', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_fixed_assets', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_intangible_assets', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_other_assets', models.DecimalField(decimal_places=2, max_digits=10)),
                ('client_savings', models.DecimalField(decimal_places=2, max_digits=10)),
                ('account_payable', models.DecimalField(decimal_places=2, max_digits=10)),
                ('wages_payable', models.DecimalField(decimal_places=2, max_digits=10)),
                ('short_term_borrowing', models.DecimalField(decimal_places=2, max_digits=10)),
                ('long_term_debt_commercial_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('long_term_debt_concessional_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('other_accrued_expenses', models.DecimalField(decimal_places=2, max_digits=10)),
                ('income_taxes_payable', models.DecimalField(decimal_places=2, max_digits=10)),
                ('restricted_revenue', models.DecimalField(decimal_places=2, max_digits=10)),
                ('loan_fund_capital', models.DecimalField(decimal_places=2, max_digits=10)),
                ('retained_net_surplus', models.DecimalField(decimal_places=2, max_digits=10)),
                ('net_surplus', models.DecimalField(decimal_places=2, max_digits=10)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='balance_sheet_branch', to='accounts.Branch')),
            ],
        ),
    ]
