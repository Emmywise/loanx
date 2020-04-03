# Generated by Django 3.0.3 on 2020-04-03 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0007_auto_20200403_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanrepayment',
            name='loan_schedule',
        ),
        migrations.AddField(
            model_name='loanrepayment',
            name='loan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='loans.Loan'),
            preserve_default=False,
        ),
    ]
