from django.contrib import admin
from Employee.models import Employee, Address, EmpAddress, HRPaymentTable, Leave
from django import forms

# Register your models here.
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm
    list_display = ('eid', 'ename', 'eemail', 'econtact', 'department', 'etype', 'desination', 'salary')

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ('eid', 'leave_type', 'leave_quota', 'leave_availed', 'created_by')

class LeaveAdmin(admin.ModelAdmin):
    form = LeaveForm
    list_display = ('eid', 'leave_type', 'leave_quota', 'leave_balance')

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Address)
admin.site.register(EmpAddress)
admin.site.register(HRPaymentTable)
admin.site.register(Leave, LeaveAdmin)
