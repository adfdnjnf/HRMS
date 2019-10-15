# Generated by Django 2.2.4 on 2019-10-15 05:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(max_length=1024, verbose_name='Address line 1')),
                ('address2', models.CharField(max_length=1024, verbose_name='Address line 2')),
                ('zip_code', models.IntegerField(verbose_name='ZIP / Postal code')),
                ('city', models.CharField(max_length=1024, verbose_name='City')),
                ('country', models.CharField(max_length=10, verbose_name='Country')),
                ('contact_number', models.BigIntegerField(verbose_name='contact_number')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eid', models.CharField(max_length=20)),
                ('doj', models.DateField()),
                ('ename', models.CharField(max_length=100)),
                ('eemail', models.EmailField(max_length=254)),
                ('econtact', models.BigIntegerField()),
                ('department', models.CharField(max_length=20)),
                ('etype', models.CharField(max_length=20)),
                ('desination', models.CharField(max_length=30)),
                ('salary', models.IntegerField()),
            ],
            options={
                'db_table': 'Employee',
            },
        ),
        migrations.CreateModel(
            name='HRPaymentTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eid', models.CharField(help_text='eid', max_length=10)),
                ('ctc', models.IntegerField(help_text='P/A')),
                ('hra', models.IntegerField(help_text='House Rent Allowance')),
                ('professional_tax', models.IntegerField(help_text='Professional Tax')),
                ('gross_amount', models.IntegerField(help_text='Gross amount P/M')),
                ('net_amount', models.IntegerField(help_text='Net amount P/M')),
                ('pf_deduction', models.IntegerField(help_text='Provident Fund')),
                ('total_deduction', models.FloatField(help_text='Total deduction')),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_foreign_key', models.IntegerField()),
                ('tran_date', models.DateField()),
                ('tran_type', models.CharField(choices=[('leave', 'leave')], max_length=20)),
                ('eid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(choices=[('PL', 'Privilege Leave'), ('CL', 'Casual Leave'), ('SL', 'Sick Leave')], max_length=2)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('no_of_days', models.IntegerField()),
                ('leave_reason', models.CharField(choices=[('Personal', 'Personal'), ('Vacation', 'Vacation'), ('Marriage', 'Marriage'), ('Sick Leave', 'Sick Leave'), ('Family', 'Family'), ('Others', 'Others')], max_length=20)),
                ('creation_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('eid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(choices=[('PL', 'Privilege Leave'), ('CL', 'Casual Leave'), ('SL', 'Sick Leave')], max_length=2)),
                ('leave_quota', models.IntegerField()),
                ('leave_availed', models.IntegerField(default=0)),
                ('leave_balance', models.IntegerField()),
                ('leave_carryforward', models.IntegerField(default=0)),
                ('creation_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('eid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmpAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PermanentAddress', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='PermanentAddress', to='Employee.Address')),
                ('PrimaryAddress', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='PrimaryAddress', to='Employee.Address')),
                ('operator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Employee.Employee')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Employee.EmpAddress')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='eid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.Employee'),
        ),
    ]
