from django.db import models
#from .models import PrimaryAddress, PermanentAddress
#from django.db.models import F, Sum
from django.utils import timezone
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

class Employee(models.Model):
    eid = models.CharField(max_length=20)
    doj = models.DateField()
    ename = models.CharField(max_length=100)
    eemail = models.EmailField()
    econtact = models.BigIntegerField()
    department = models.CharField(max_length=20)
    etype = models.CharField(max_length=20)
    desination = models.CharField(max_length=30)
    salary = models.IntegerField()

    class Meta:
        db_table = "Employee"

class Address(models.Model):
    eid = models.ForeignKey('Employee', on_delete=models.CASCADE)
    address1 = models.CharField("Address line 1", max_length=1024, )
    address2 = models.CharField("Address line 2", max_length=1024, )
    zip_code = models.IntegerField("ZIP / Postal code")
    city = models.CharField("City", max_length=1024, )
    country = models.CharField("Country", max_length=10, )
    contact_number = models.BigIntegerField("contact_number")

class EmpAddress(models.Model):
    status = models.ForeignKey('EmpAddress', null=True, on_delete=models.SET_NULL)
    operator = models.ForeignKey('Employee', null=True, on_delete=models.SET_NULL)
    PrimaryAddress = models.ForeignKey('Address', related_name='PrimaryAddress', null=True, on_delete=models.SET_NULL, blank=True)
    PermanentAddress = models.ForeignKey(Address, related_name='PermanentAddress', null=True, on_delete=models.SET_NULL, blank=True)


class HRPaymentTable(models.Model):
    eid = models.CharField(max_length=10, help_text='eid')
    ctc = models.IntegerField(help_text='P/A')
    hra = models.IntegerField(help_text='House Rent Allowance')
    professional_tax = models.IntegerField(help_text='Professional Tax')
    gross_amount = models.IntegerField(help_text='Gross amount P/M')
    net_amount = models.IntegerField(help_text='Net amount P/M')
    pf_deduction = models.IntegerField(help_text='Provident Fund')
    total_deduction = models.FloatField(help_text='Total deduction')

class Leave(models.Model):
    LEAVE_TYPE_CHOICE = (
                    ('PL', 'Privilege Leave'),
                    ('CL', 'Casual Leave'),
                    ('SL', 'Sick Leave'),
    )
    eid = models.ForeignKey('Employee', on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=2, choices=LEAVE_TYPE_CHOICE)
    leave_quota = models.IntegerField()
    leave_availed = models.IntegerField(default=0)
    leave_balance = models.IntegerField()
    leave_carryforward = models.IntegerField(default=0)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    creation_timestamp = models.DateTimeField(default=timezone.now)

    def calculate_leave_balance(self):
        '''Re-calculates and sets the correct values for
            all the fields in the Leave Model
        '''
        self.leave_balance = self.leave_quota - self.leave_availed
        self.save()

    def publish(self):
        try:
            self.full_clean()
        except ValidationError as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        self.save()

    def __str__(self):
        return self.eid.name

    def clean(self):
        errordict = {}
        today = timezone.localdate()
        # if (self.doj > today):
        #     errordict['doj'] = 'Date of Joining cannot be in future'

        #Pass the Dictionary to raise ValidationError
        self.calculate_leave_balance()
        raise ValidationError(errordict)

#    def applyLeave(self):

class LeaveTransaction(models.Model):
    LEAVE_TYPE_CHOICES = (
                    ('PL', 'Privilege Leave'),
                    ('CL', 'Casual Leave'),
                    ('SL', 'Sick Leave'),
    )
    LEAVE_REASON_CHOICES = (
                    ('Personal', 'Personal'),
                    ('Vacation', 'Vacation'),
                    ('Marriage', 'Marriage'),
                    ('Sick Leave', 'Sick Leave'),
                    ('Family', 'Family'),
                    ('Others', 'Others'),
    )
    eid = models.ForeignKey('Employee', on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=2, choices=LEAVE_TYPE_CHOICES)
    from_date = models.DateField()
    to_date = models.DateField()
    no_of_days = models.IntegerField()
    leave_reason = models.CharField(max_length=20, choices=LEAVE_REASON_CHOICES)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    creation_timestamp = models.DateTimeField(default=timezone.now)

    def publish(self):
        try:
            self.full_clean()
        except ValidationError as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        self.save()

    # def __str__(self):
    #     return str(self.emp_id.name)+'_'+str(self.leave_type)

    def clean(self):
        errordict = {}
        today = timezone.localdate  ()
        if (self.from_date > self.to_date):
             errordict['from_date'] = 'From Date cannot be greater than To date'
        #if (self.leave_reason == 'Marriage' and self.eid.marital_status == True):
            #errordict['leave_reason'] = 'You are already married'
        #Pass the Dictionary to raise ValidationError
        raise ValidationError(errordict)


class Transactions(models.Model):
    TRANSACTION_TYPE_CHOICE = (
        ('leave', 'leave'),

    )
    eid = models.ForeignKey('Employee', on_delete=models.CASCADE)
    model_foreign_key = models.IntegerField()
    tran_date = models.DateField()
    tran_type = models.CharField(max_length=20,
                                 choices=TRANSACTION_TYPE_CHOICE
                                 )

    def add_ledger(self, eid, tran_type, model_foreign_key):
        self.eid = eid
        self.tran_type = tran_type
        self.model_foreign_key = model_foreign_key
        self.tran_date = timezone.now()
        self.save()

    def publish(self):
        try:
            self.full_clean()
        except ValidationError as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        self.save()

    def __str__(self):
        return self.eid.name

    def clean(self):
        errordict = {}
        today = timezone.localdate()
        # if (self.doj > today):
        #     errordict['doj'] = 'Date of Joining cannot be in future'

        # Pass the Dictionary to raise ValidationError
        raise ValidationError(errordict)
