# Generated by Django 3.0.3 on 2020-03-26 06:29

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200324_1113'),
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=125)),
                ('when_date', models.DateTimeField()),
                ('from_date', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Branch')),
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
            name='CalendarLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_type', models.CharField(choices=[('Disbursed', 'Disbursed'), ('Due Amount', 'Due Amount'), ('Maturity', 'Maturity'), ('Payment Schedule', 'Payment Schedule')], max_length=100)),
                ('url_path', models.CharField(max_length=400)),
                ('date', models.DateTimeField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='CalendarEventEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=225)),
                ('calendar_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.CalendarEvent')),
            ],
        ),
    ]
