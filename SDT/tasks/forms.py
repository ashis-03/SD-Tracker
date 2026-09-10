from django import forms
from .models import Task
from employees.models import Employee

# Create Task
class TaskForm(forms.ModelForm):

    class Meta:

        model = Task

        fields = [
            "title",
            "description",
            "project",
            "phase",
            "assigned_to",
            "deadline",
            "priority",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter task title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe the task"
                }
            ),

            "project": forms.Select(
                attrs={"class": "form-control"}
            ),

            "phase": forms.Select(
                attrs={"class": "form-control"}
            ),

            "assigned_to": forms.Select(
                attrs={"class": "form-control"}
            ),

            "deadline": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "priority": forms.Select(
                attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
    
        super().__init__(*args, **kwargs)

        # Only Project Managers can be selected
        self.fields["assigned_to"].queryset = Employee.objects.filter(
            user__profile__role="employee"
        )


# Edit Task - Admin / Manager
class TaskEditForm(forms.ModelForm):

    class Meta:

        model = Task

        fields = [
            "title",
            "description",
            "phase",
            "assigned_to",
            "deadline",
            "priority",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),

            "phase": forms.Select(
                attrs={"class": "form-control"}
            ),

            "assigned_to": forms.Select(
                attrs={"class": "form-control"}
            ),

            "deadline": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "priority": forms.Select(
                attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        
            super().__init__(*args, **kwargs)
    
            # Only Project Managers can be selected
            self.fields["assigned_to"].queryset = Employee.objects.filter(
                user__profile__role="employee"
            )


# Employee updates progress
class TaskUpdateForm(forms.ModelForm):

    class Meta:

        model = Task

        fields = [
            "progress",
        ]

        widgets = {

            "progress": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100
                }
            ),
        }


# Employee uploads and submits work
class TaskSubmissionForm(forms.ModelForm):

    class Meta:

        model = Task

        fields = [
            "work_file",
        ]

        widgets = {

            "work_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }