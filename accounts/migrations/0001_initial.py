# Generated by Django 3.1.2 on 2020-11-06 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('open_date', models.DateField()),
                ('currency', models.CharField(max_length=10)),
                ('date_format', models.CharField(choices=[('dd/mm/yyyy', '%d/%m/%Y'), ('mm/dd/yyyy', '%m/%d/%Y'), ('yyyy/mm/dd', '%Y/%m/%d')], max_length=20)),
                ('currency_in_words', models.CharField(max_length=225)),
                ('address', models.CharField(blank=True, max_length=400, null=True)),
                ('city', models.CharField(blank=True, max_length=400, null=True)),
                ('landline', models.CharField(blank=True, max_length=20, null=True)),
                ('mobile', models.IntegerField(blank=True, null=True)),
                ('min_loan_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('max_loan_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('min_loan_interest', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('max_loan_interest', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('is_friday_branch_holiday', models.BooleanField(default=False)),
                ('is_saturday_branch_holiday', models.BooleanField(default=False)),
                ('is_sunday_branch_holiday', models.BooleanField(default=False)),
                ('holiday_effect_on_loan_schedule', models.CharField(choices=[('Next day that is not a holiday', 'Next day that is not a holiday'), ('Next Repayment Cycle', 'Next Repayment Cycle')], max_length=100)),
                ('capital', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('loan_generate_string', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125)),
                ('capital', models.CharField(max_length=125)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('active', models.BooleanField(default=False)),
                ('user_type', models.CharField(choices=[('admin', 'admin'), ('staff', 'staff'), ('customer', 'customer')], max_length=20)),
                ('is_super_admin', models.BooleanField(default=False)),
                ('activation_token', models.CharField(blank=True, max_length=100, null=True)),
                ('esignature', models.FileField(blank=True, null=True, upload_to='esignature')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.branch')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BranchHoliday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.branch')),
            ],
        ),
        migrations.CreateModel(
            name='BranchAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.branch')),
            ],
        ),
        migrations.AddField(
            model_name='branch',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.country'),
        ),
        migrations.CreateModel(
            name='AccountResetLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reset_token', models.CharField(blank=True, max_length=400, null=True, unique=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
