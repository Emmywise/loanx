# Generated by Django 3.0.3 on 2020-03-25 11:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_auto_20200324_1113'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashSafeManagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='CashSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225, unique=True)),
                ('bank_balance_cash', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('bank_balance_coins', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('total_balance', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('cash_safe_management', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='savings_investments.CashSafeManagement')),
            ],
        ),
        migrations.CreateModel(
            name='SavingsAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('savings_id', models.CharField(blank=True, max_length=125, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('available_balance', models.DecimalField(decimal_places=2, max_digits=100)),
                ('ledger_balance', models.DecimalField(decimal_places=2, max_digits=100)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Branch')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='TransferCash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_notes', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('amount_coins', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('cash_safe_management', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='savings_investments.CashSafeManagement')),
                ('from_cash_source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_cash_source', to='savings_investments.CashSource')),
                ('from_teller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_teller', to='savings_investments.CashSource')),
                ('to_cash_source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_cash_source', to='savings_investments.CashSource')),
                ('to_teller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_teller', to='savings_investments.CashSource')),
            ],
        ),
        migrations.CreateModel(
            name='Teller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('debit_notes', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('debit_coins', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('credit_notes', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('credit_coins', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('total_balance', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('cash_safe_management', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='savings_investments.CashSafeManagement')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='SavingsTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('transaction_type', models.CharField(choices=[('Deposit', 'Deposit'), ('Withdrawal', 'Withdrawal'), ('Bank Fee', 'Bank Fee'), ('Interest', 'Interest'), ('Dividend', 'Dividend'), ('Transfer In', 'Transfer In'), ('Transfer Out', 'Transfer Out'), ('Commission', 'Commission')], max_length=100)),
                ('date_time', models.DateTimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Branch')),
                ('savings_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='savings_investments.SavingsAccount')),
                ('teller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='savings_investments.Teller')),
            ],
        ),
        migrations.CreateModel(
            name='SavingsProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125)),
                ('interest_rate_per_anum', models.DecimalField(decimal_places=2, max_digits=10)),
                ('interest_method', models.CharField(choices=[('Last Savings Balance', 'Last Savings Balance'), ('Pro-Rata Basis', 'Pro-Rata Basis')], max_length=100)),
                ('interest_posting_frequency', models.CharField(blank=True, max_length=300, null=True)),
                ('interest_addition_time', models.CharField(blank=True, max_length=300, null=True)),
                ('min_balance_for_interest', models.DecimalField(decimal_places=2, max_digits=100)),
                ('overdrawn', models.BooleanField(default=False)),
                ('min_balance_for_withdrawal', models.DecimalField(decimal_places=2, max_digits=100)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Branch')),
            ],
        ),
        migrations.AddField(
            model_name='savingsaccount',
            name='savings_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='savings_investments.SavingsProduct'),
        ),
        migrations.CreateModel(
            name='CustomSavingsAccountField',
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
                ('file_upload', models.FileField(blank=True, null=True, upload_to='savings_accounts')),
                ('savings_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='savings_investments.SavingsAccount')),
            ],
        ),
    ]