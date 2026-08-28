from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    role = request.user.profile.role

    if role == "admin":
        return render(request,"dashboard/admin_dashboard.html")

    elif role == "manager":
        return render(request,"dashboard/manager_dashboard.html")

    elif role == "employee":
        return render(request,"dashboard/employee_dashboard.html")

    return render(request,"dashboard/employee_dashboard.html")