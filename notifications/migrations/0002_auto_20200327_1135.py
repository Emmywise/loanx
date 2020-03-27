# Generated by Django 3.0.3 on 2020-03-27 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sendsms',
            name='message',
        ),
        migrations.AlterField(
            model_name='sendsms',
            name='message_purpose',
            field=models.CharField(choices=[('to_all_borrowers', 'to_all_borrowers'), ('delivered', 'delivered'), ('failed', 'failed')], max_length=100),
        ),
        migrations.AlterField(
            model_name='sendsms',
            name='status',
            field=models.CharField(choices=[('sent', 'sent'), ('pending', 'pending'), ('failed', 'failed')], max_length=100),
        ),
    ]
