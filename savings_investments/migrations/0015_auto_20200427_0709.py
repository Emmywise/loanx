# Generated by Django 3.0 on 2020-04-27 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_branch_capital'),
        ('savings_investments', '0014_savingstransaction_account_to_account_transfer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashsafemanagement',
            name='branch',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.Branch'),
        ),
    ]