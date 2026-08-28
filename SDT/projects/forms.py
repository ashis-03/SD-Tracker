from django import forms
from .models import Project
from .models import Employee

class ProjectForm(forms.ModelForm):

    class Meta:

        model = Project

        fields = [
            "name",
            "description",
            "client_name",
            "start_date",
            "deadline",
            "status",
            "manager",
            "teams",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter project name"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter project description"
                }
            ),

            "client_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter client name"
                }
            ),

            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "deadline": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "manager": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "teams": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Only Project Managers can be selected
        self.fields["manager"].queryset = Employee.objects.filter(
            user__profile__role="manager"
        )