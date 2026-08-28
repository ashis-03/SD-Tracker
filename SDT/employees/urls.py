from django.urls import path
from . import views


urlpatterns = [
# Employee
path("",views.employee_list,name="employee_list"),
path("<int:pk>/",views.employee_detail,name="employee_detail"),
path("add/",views.employee_create,name="employee_create"),
path("<int:pk>/edit/",views.employee_update,name="employee_update"),
path("<int:pk>/delete/",views.employee_delete,name="employee_delete"),
# Team
path("teams/",views.team_list,name="team_list"),
path("teams/<int:pk>/",views.team_detail,name="team_detail"),
path("teams/add/",views.team_create,name="team_create"),
path("teams/<int:pk>/edit/",views.team_update,name="team_update"),
path("teams/<int:pk>/delete/",views.team_delete,name="team_delete"),
]