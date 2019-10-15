from django.conf.urls import url
from Employee import views

# SET THE NAMESPACE!
app_name = 'Employee'

# Be careful setting the name to just /login use userlogin

urlpatterns = [
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^EmpAddress/$', views.EmpAddress, name='EmpAddress'),
    url(r'^applyleave/(?P<eid>\d+)/$', views.applyleave, name='applyleave')

]