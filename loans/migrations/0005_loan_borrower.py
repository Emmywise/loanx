# Generated by Django 3.0.3 on 2020-03-25 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0001_initial'),
        ('loans', '0004_auto_20200325_0519'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='borrower',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='borrowers.Borrower'),
            preserve_default=False,
        ),
    ]
