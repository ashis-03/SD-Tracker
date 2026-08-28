from django.db import models
from employees.models import Employee, Team
from django.core.validators import MaxValueValidator

class Project(models.Model):

    STATUS_CHOICES = (
        ("planning", "Planning"),
        ("active", "Active"),
        ("on_hold", "On Hold"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    name = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    client_name = models.CharField(
        max_length=150
    )

    start_date = models.DateField()

    deadline = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning"
    )

    manager = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        related_name="managed_projects"
    )

    progress = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)]
    )

    # Team working on this project
    teams = models.ManyToManyField(
        Team,
        related_name="projects",
        blank=True
    )

    def update_progress(self):
        # Get all SDLC phases belonging to this project
        phases = self.phases.all()

        total_phases = phases.count()

        if total_phases == 0:
            self.progress = 0

        else:
            total_progress = sum(
                phase.progress for phase in phases
            )

            self.progress = round(
                total_progress / total_phases
            )

        if self.progress == 100:
            self.status = "completed"

        self.save()

    def __str__(self):
        return self.name