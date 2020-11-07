# Generated by Django 3.1.2 on 2020-11-06 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.OneToOneField(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_pay', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('overtime_pay', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('paid_leaves', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('transport_allowance', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('medical_allowance', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('bonus', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('other_allowances', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('total_pay', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('pension', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('health_insurance', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('unpaid_leave', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('tax_deduction', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('salary_loan', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('total_deduction', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('net_pay', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('payment_method', models.CharField(blank=True, max_length=100, null=True)),
                ('is_recurring', models.BooleanField(default=False)),
                ('recurring_date', models.CharField(blank=True, max_length=125, null=True)),
                ('send_slip_to_staff_email', models.BooleanField(default=False)),
                ('pay_date', models.DateField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.branch')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
        ),
    ]
