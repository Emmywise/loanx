# Generated by Django 3.1.2 on 2020-10-28 09:20

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=400)),
                ('middle_name', models.CharField(max_length=400)),
                ('last_name', models.CharField(max_length=400)),
                ('business_name', models.CharField(blank=True, max_length=400, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')], max_length=100)),
                ('title', models.CharField(choices=[('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Dr', 'Dr'), ('Ms', 'Ms'), ('Rev', 'Rev')], max_length=100)),
                ('mobile', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=100)),
                ('date_of_birth', models.CharField(max_length=400)),
                ('address', models.CharField(max_length=400)),
                ('city', models.CharField(max_length=400)),
                ('state', models.CharField(max_length=400)),
                ('zip_code', models.CharField(blank=True, max_length=400, null=True)),
                ('land_line', models.CharField(blank=True, max_length=400, null=True)),
                ('working_status', models.CharField(choices=[('Employer', 'Employer'), ('Government Employee', 'Government Employee'), ('Private Sector', 'Private Sector'), ('Employee', 'Employee'), ('Owner', 'Owner'), ('Student', 'Student'), ('Overseas Worker', 'Overseas Worker'), ('Pensioner', 'Pensioner'), ('Unemployed', 'Unemployed')], max_length=100)),
                ('borrower_photo', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('description', models.CharField(max_length=400)),
                ('is_activated', models.BooleanField(default=False)),
                ('loan_score', models.PositiveIntegerField(blank=True, null=True)),
                ('profile', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
        ),
        migrations.CreateModel(
            name='BorrowerGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=255)),
                ('meeting_date', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('group_leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='group_leader', to='borrowers.borrower')),
            ],
        ),
        migrations.CreateModel(
            name='InviteBorrower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='borrowers.borrower')),
                ('borrower_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='borrowers.borrowergroup')),
            ],
        ),
        migrations.AddField(
            model_name='borrowergroup',
            name='members',
            field=models.ManyToManyField(through='borrowers.Membership', to='borrowers.Borrower'),
        ),
    ]
