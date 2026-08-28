from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("on_leave", "On Leave"),
        ("inactive", "Inactive"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee"
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True
    )

    designation = models.CharField(
        max_length=100
    )

    department = models.CharField(
        max_length=100
    )

    skills = models.TextField(
        blank=True
    )

    joining_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"


# Teams
class Team(models.Model):

    name = models.CharField(
        max_length=100
    )

    manager = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_teams"
    )

    members = models.ManyToManyField(
        Employee,
        related_name="teams",
        blank=True
    )

    def __str__(self):
        return self.name