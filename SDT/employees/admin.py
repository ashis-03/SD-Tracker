from django.contrib import admin
from .models import Employee, Team


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = [
        "employee_id",
        "get_full_name",
        "designation",
        "department",
        "joining_date",
        "status",
    ]

    list_filter = [
        "department",
        "status",
    ]

    search_fields = [
        "employee_id",
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    ]

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    get_full_name.short_description = "Employee Name"


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "manager",
    ]

    search_fields = [
        "name",
    ]

    filter_horizontal = [
        "members",
    ]