from django import forms
from .models import Employee, Team
from django.contrib.auth.models import User


# EMP FORM
class EmployeeForm(forms.ModelForm):

    role = forms.ChoiceField(
        choices=[
            ("employee", "Employee"),
            ("manager", "Project Manager"),
            ("admin", "Admin"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = Employee

        fields = [
            "user",
            "employee_id",
            "designation",
            "department",
            "skills",
            "joining_date",
            "status",
        ]

        widgets = {
            "joining_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # CREATE EMPLOYEE
        if not self.instance.pk:

            # Show only users who don't already have
            # an Employee profile
            self.fields["user"].queryset = User.objects.filter(
                employee__isnull=True
            )

            # Default role
            self.fields["role"].initial = "employee"

        # EDIT EMPLOYEE
        else:

            # Show unassigned users + current employee's user
            self.fields["user"].queryset = (
                User.objects.filter(employee__isnull=True)
                | User.objects.filter(
                    pk=self.instance.user.pk
                )
            )

            # Show current role
            if hasattr(self.instance.user, "profile"):

                self.fields["role"].initial = (
                    self.instance.user.profile.role
                )


# TEAM FORM
class TeamForm(forms.ModelForm):

    class Meta:
        model = Team

        fields = [
            "name",
            "manager",
            "members"
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter team name"
                }
            ),

            "manager": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

           "members": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Only Project Managers can be selected as manager
        self.fields["manager"].queryset = Employee.objects.filter(
            user__profile__role="manager"
        )

        # Only Employees can be added as team members
        self.fields["members"].queryset = Employee.objects.filter(
            user__profile__role="employee"
        )