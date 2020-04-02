# Generated by Django 3.0.3 on 2020-04-02 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0008_auto_20200401_2328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrower',
            name='borrower_group',
        ),
        migrations.AddField(
            model_name='borrowergroup',
            name='member',
            field=models.ManyToManyField(to='borrowers.Borrower'),
        ),
        migrations.AlterField(
            model_name='borrowergroup',
            name='group_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='group_leader', to='borrowers.Borrower'),
        ),
    ]
