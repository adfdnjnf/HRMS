import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from Employee.forms import LeaveTransactionForm, AddressForm, EmpAddressForm
from Employee.models import Leave, Employee, LeaveTransaction, Transactions
from django.db import transaction
from django.views import View


def index(request):
    return render(request, 'Employee/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'Employee/login.html', {})

logger=logging.getLogger(__name__)


def applyleave(request, eid):
    if request.method == "POST":
        leavetransaction = LeaveTransactionForm(request.POST)
        if leavetransaction.is_valid():
            saved_leavetransaction = leavetransaction.save(commit=False)
            leave = get_object_or_404(
                                    Leave,
                                    eid=eid,
                                    leave_type=saved_leavetransaction.leave_type
                                )
            saved_leavetransaction.no_of_days = (saved_leavetransaction.to_date-saved_leavetransaction.from_date).days
            if(leave.leave_balance <= saved_leavetransaction.no_of_days):
                raise ValidationError({'leave_type':'You do not have sufficient leave balance'})
            else:
                leave.leave_balance = leave.leave_quota - saved_leavetransaction.no_of_days
                leave.leave_availed = saved_leavetransaction.no_of_days
#                leave.calculate_leave_balance()
                saved_leavetransaction.emp_id = Employee.objects.get(id=eid)
#                saved_leavetransaction.no_of_days = saved_leavetransaction.from_date-leavetransaction.to_date
                saved_leavetransaction.created_by = request.user
                saved_leavetransaction.creation_timestamp = timezone.now()
                saved_leavetransaction.save()
                leave.save()
                transaction = Transactions()
                transaction.add_ledger(eid=Employee.objects.get(id=eid),
                                    tran_type='leave',
                                    model_foreign_key=saved_leavetransaction.id
                )
                return redirect('leave_details', pk=saved_leavetransaction.id)
    else:
        leavetransaction = LeaveTransactionForm()
        return render(request, 'Employee/applyleave.html',
                        {'leavetransaction':leavetransaction, 'Employee': Employee.objects.get(id=eid)}
                )

def EmpAddress(request):
    if request.method == 'POST':
       EmpAddress_form = EmpAddressForm(request.POST, request.FILES)
       EmpAddress_form_valid = EmpAddress_form.is_valid()
       Address_form = AddressForm(request.POST)
       Address_form_valid = Address_form.is_valid()
       PrimaryAddress_form = AddressForm(request.POST)
       PrimaryAddress_form_valid = PrimaryAddress_form.is_valid()
    # check whether it's valid:
       if EmpAddress_form_valid and Address_form_valid and PrimaryAddress_form_valid:
          print("success")
        # process the data

          with transaction.atomic():
              PermanentAddress = Address_form.save()
              PrimaryAddress = PrimaryAddress_form.save()

              EmpAddress = EmpAddress_form.save(commit=False)
              EmpAddress.PermanentAddress = PermanentAddress
              EmpAddress.PrimaryAddress = PrimaryAddress
              EmpAddress.save()

            # redirect to a new URL:
              return HttpResponseRedirect('Employee/index.html')
       else:
            print("failure")
            print(EmpAddress_form.errors)
            print(Address_form.errors)

# if a GET (or any other method) we'll create a blank form
    else:
        EmpAddress_form = EmpAddressForm()
        Address_form = AddressForm()
        PrimaryAddress_form = AddressForm()

    return render(request, 'Employee/EmpAddress.html',
              {'title': 'Employee Address', 'EmpAddress_form': EmpAddress_form,
               'Address_form': Address_form, 'PrimaryAddress_form': PrimaryAddress_form})