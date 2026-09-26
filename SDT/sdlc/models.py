from django.db import models
from projects.models import Project


class SDLCPhase(models.Model):

    PHASE_CHOICES = (
        ("requirement", "Requirement Gathering"),
        ("design", "Design"),
        ("development", "Development"),
        ("testing", "Testing"),
        ("deployment", "Deployment"),
        ("maintenance", "Maintenance"),
    )

    STATUS_CHOICES = (
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("on_hold", "On Hold"),
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="phases"
    )

    phase_name = models.CharField(
        max_length=50,
        choices=PHASE_CHOICES
    )

    description = models.TextField(
        blank=True
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    deadline = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="not_started"
    )

    progress = models.PositiveIntegerField(
        default=0
    )

    # Controls the order of phases
    order = models.PositiveIntegerField(
        default=1
    )

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["project", "phase_name"],
                name="unique_phase_per_project"
            )
        ]

    def __str__(self):
        return f"{self.project.name} - {self.get_phase_name_display()}"