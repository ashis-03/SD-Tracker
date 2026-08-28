from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Create a password"
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm your password"
        })
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "Enter your first name"
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Enter your last name"
            }),
            "username": forms.TextInput(attrs={
                "placeholder": "Choose a username"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Enter your email"
            }),
        }

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:

            if password != confirm_password:
                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data

    def clean_email(self):

        email = self.cleaned_data.get("email")

        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email already exists."
            )

        return email
    