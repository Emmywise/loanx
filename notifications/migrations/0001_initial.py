# Generated by Django 3.1.2 on 2020-11-06 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SendEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('sent', 'sent'), ('delivered', 'delivered'), ('failed', 'failed')], max_length=100)),
                ('message_purpose', models.CharField(choices=[('Message to all borrowers', 'Message to all borrowers'), ('invite new borrowers', 'invite new borrowers'), ('loan remainder', 'loan remainder'), ('successful repayment', 'successful repayment'), ('daily collection', 'daily collection'), ('e-signature', 'e-signature'), ('payroll payslip', 'payroll payslip')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SMS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('sent', 'sent'), ('pending', 'pending'), ('failed', 'failed')], max_length=100)),
                ('message_purpose', models.CharField(choices=[('to_all_borrowers', 'to_all_borrowers')], max_length=100)),
            ],
        ),
    ]
