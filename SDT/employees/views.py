from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .models import Employee, Team
from .forms import EmployeeForm, TeamForm

#  ---------------------------------------------------------
# EMPLOYEE VIEW
#  ---------------------------------------------------------

# EMP LIST
def employee_list(request):

    employees = Employee.objects.select_related("user")

    search = request.GET.get("search")

    department = request.GET.get("department")

    status = request.GET.get("status")

    if search:

        employees = employees.filter(

            Q(employee_id__icontains=search) |

            Q(user__first_name__icontains=search) |

            Q(user__last_name__icontains=search) |

            Q(user__email__icontains=search)

        )

    if department:

        employees = employees.filter(
            department=department
        )

    if status:

        employees = employees.filter(
            status=status
        )

    departments = Employee.objects.values_list(
        "department",
        flat=True
    ).distinct()

    context = {

        "employees": employees,

        "departments": departments,

        "total_employees": Employee.objects.count(),

        "active_employees":
            Employee.objects.filter(
                status="active"
            ).count(),

        "on_leave":
            Employee.objects.filter(
                status="on_leave"
            ).count(),

    }

    return render(
        request,
        "employees/employee_list.html",
        context
    )


# EMP DETAIL
def employee_detail(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    return render(
        request,
        "employees/employee_detail.html",
        {
            "employee": employee
        }
    )


# EMP ADD
def employee_create(request):

    if request.method == "POST":

        form = EmployeeForm(
            request.POST
        )

        if form.is_valid():

            employee = form.save()

            role = form.cleaned_data["role"]

            employee.user.profile.role = role

            employee.user.profile.save()

            return redirect("employee_list")

    else:

        form = EmployeeForm()

    return render(
        request,
        "employees/employee_form.html",
        {
            "form": form,
            "title": "Add Employee"
        }
    )


# EMP EDIT
def employee_update(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    # Store the old role before updating
    old_role = employee.user.profile.role

    if request.method == "POST":

        form = EmployeeForm(
            request.POST,
            instance=employee
        )

        if form.is_valid():

            employee = form.save()

            # Get newly selected role
            new_role = form.cleaned_data["role"]

            # Update role
            employee.user.profile.role = new_role
            employee.user.profile.save()

            return redirect("employee_list")

    else:

        form = EmployeeForm(
            instance=employee
        )

    return render(
        request,
        "employees/employee_form.html",
        {
            "form": form,
             "title": "Edit Employee"
        }
    )


# EMP DELETE
def employee_delete(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    if request.method == "POST":

        employee.delete()

        return redirect(
            "employee_list"
        )

    return render(
        request,
        "employees/employee_confirm_delete.html",
        {
            "employee": employee
        }
    )

#  ---------------------------------------------------------
# TEAM VIEW
#  ---------------------------------------------------------


# Team List
from django.db.models import Q

def team_list(request):

    teams = Team.objects.all()

    # =========================
    # SEARCH
    # =========================

    search = request.GET.get("search", "").strip()

    if search:
        teams = teams.filter(
            Q(name__icontains=search) |
            Q(manager__user__first_name__icontains=search) |
            Q(manager__user__last_name__icontains=search) |
            Q(manager__user__username__icontains=search) |
            Q(manager__user__email__icontains=search)
        ).distinct()

    # =========================
    # STATISTICS
    # =========================

    total_members = Employee.objects.filter(
        teams__in=Team.objects.all()
    ).distinct().count()

    total_managers = Team.objects.exclude(
        manager=None
    ).count()

    active_teams = Team.objects.count()

    context = {
        "teams": teams,
        "total_members": total_members,
        "total_managers": total_managers,
        "active_teams": active_teams,
        "search": search,
    }

    return render(
        request,
        "employees/teams/team_list.html",
        context
    )


# Create Team
def team_create(request):

    if request.method == "POST":

        form = TeamForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Team created successfully."
            )

            return redirect("team_list")

    else:

        form = TeamForm()

    return render(
        request,
        "employees/teams/team_form.html",
        {
            "form": form,
            "title": "Create Team"
        }
    )


# Team Detail
def team_detail(request, pk):

    team = get_object_or_404(
        Team.objects.select_related(
            "manager__user"
        ).prefetch_related(
            "members__user"
        ),
        pk=pk
    )

    return render(
        request,
        "employees/teams/team_detail.html",
        {
            "team": team
        }
    )


# Edit Team
def team_update(request, pk):

    team = get_object_or_404(
        Team,
        pk=pk
    )

    if request.method == "POST":

        form = TeamForm(
            request.POST,
            instance=team
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Team updated successfully."
            )

            return redirect(
                "team_detail",
                pk=team.pk
            )

    else:

        form = TeamForm(
            instance=team
        )

    return render(
        request,
        "employees/teams/team_form.html",
        {
            "form": form,
            "title": "Edit Team"
        }
    )


# Delete Team 
def team_delete(request, pk):

    team = get_object_or_404(
        Team,
        pk=pk
    )

    if request.method == "POST":

        team.delete()

        messages.success(
            request,
            "Team deleted successfully."
        )

        return redirect("team_list")

    return render(
        request,
        "employees/teams/team_confirm_delete.html",
        {
            "team": team
        }
    )