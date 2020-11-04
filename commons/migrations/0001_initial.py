# Generated by Django 3.1.2 on 2020-11-04 09:02

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
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('purchased_date', models.DateField(blank=True, null=True)),
                ('purchased_price', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('replacement_value', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('serial_number', models.CharField(blank=True, max_length=400, null=True)),
                ('bought_from', models.CharField(blank=True, max_length=400, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssetType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('date', models.DateField()),
                ('is_recurring', models.BooleanField(default=False)),
                ('recurring_time', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.branch')),
            ],
        ),
        migrations.CreateModel(
            name='ExpensesType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=125)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='expenses')),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.expense')),
            ],
        ),
        migrations.AddField(
            model_name='expense',
            name='expenses_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.expensestype'),
        ),
        migrations.CreateModel(
            name='CustomExpenseField',
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
                ('file_upload', models.FileField(blank=True, null=True, upload_to='expenses')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.expense')),
            ],
        ),
        migrations.CreateModel(
            name='CustomAssetField',
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
                ('file_upload', models.FileField(blank=True, null=True, upload_to='asset')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.asset')),
            ],
        ),
        migrations.CreateModel(
            name='AssetValuation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valuation_date', models.DateField()),
                ('value_amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.asset')),
            ],
        ),
        migrations.CreateModel(
            name='AssetDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='assets')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.asset')),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='asset_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='commons.assettype'),
        ),
        migrations.AddField(
            model_name='asset',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.branch'),
        ),
    ]
