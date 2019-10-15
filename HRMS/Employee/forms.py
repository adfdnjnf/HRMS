from django import forms
from django.forms import ModelForm
from Employee.models import Employee, Address, EmpAddress, HRPaymentTable, LeaveTransaction



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"

class EmpAddressForm(forms.ModelForm):
    class Meta:
        model = EmpAddress
        fields = "__all__"

class HRPaymentTableForm(forms.ModelForm):
    class Meta:
        model = HRPaymentTable
        fields = "__all__"

class DateInput(forms.DateInput):
    input_type = 'date'

class LeaveTransactionForm(forms.ModelForm):
    class Meta:
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
        model = LeaveTransaction
        exclude = ('eid', 'created_by', 'creation_timestamp', 'no_of_days')
        widgets = {
            'from_date': DateInput(),
            'to_date': DateInput(),
            'leave_reason': forms.Select(choices=LEAVE_REASON_CHOICES),
            'leave_type': forms.Select(choices=LEAVE_TYPE_CHOICES)
        }
