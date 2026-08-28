from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from projects.models import Project
from employees.models import Employee
from sdlc.models import SDLCPhase


class Task(models.Model):

    STATUS_CHOICES = (
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("in_review", "In Review"),
        ("completed", "Completed"),
        ("overdue", "Overdue"),
    )

    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    )

    REVIEW_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("changes_requested", "Changes Requested"),
        ("rejected", "Rejected"),
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    phase = models.ForeignKey(
        SDLCPhase,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks"
    )

    assigned_to = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks"
    )

    deadline = models.DateField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="todo"
    )

    progress = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    work_file = models.FileField(
        upload_to="task_work/",
        blank=True,
        null=True
    )

    submitted_at = models.DateTimeField(
        blank=True,
        null=True
    )

    review_status = models.CharField(
        max_length=30,
        choices=REVIEW_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.title