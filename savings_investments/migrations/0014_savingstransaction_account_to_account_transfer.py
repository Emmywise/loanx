# Generated by Django 3.0.3 on 2020-04-15 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings_investments', '0013_auto_20200415_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='savingstransaction',
            name='account_to_account_transfer',
            field=models.BooleanField(default=False),
        ),
    ]
