# Generated by Django 3.0.3 on 2020-04-20 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0002_inviteborrowers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InviteBorrowers',
            new_name='InviteBorrower',
        ),
    ]