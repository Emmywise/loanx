# Generated by Django 3.0.3 on 2020-04-21 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0013_auto_20200410_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='interest_type',
        ),
        migrations.AddField(
            model_name='loan',
            name='interest_method',
            field=models.CharField(choices=[('Flat Rate', 'Flat Rate'), ('Reducing Balance - Equal Installments', 'Reducing Balance - Equal Installments'), ('Reducing Balance - Equal Principal', 'Reducing Balance - Equal Principal'), ('Interest-Only', ' Interest-Only'), ('Compound-Interest', 'Compound Interest')], default='Flat Rate', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loan',
            name='interest_mode',
            field=models.CharField(blank=True, choices=[('Percentage Based', 'Percentage Based'), ('Fixed Amount Per Cycle', 'Fixed Amount Per Cycle')], max_length=400, null=True),
        ),
    ]