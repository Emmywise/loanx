# Generated by Django 3.1.2 on 2020-11-11 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0015_auto_20201111_1438'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loanrepayment',
            old_name='interest',
            new_name='interest_paid',
        ),
    ]