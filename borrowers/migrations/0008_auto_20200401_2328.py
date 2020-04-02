# Generated by Django 3.0.3 on 2020-04-01 23:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0007_auto_20200401_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowergroup',
            name='group_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='borrowers.Borrower'),
        ),
        migrations.AlterField(
            model_name='borrowergroup',
            name='group_name',
            field=models.CharField(default='mtc', max_length=255),
            preserve_default=False,
        ),
    ]
