from django.db.models.signals import post_save
from django.dispatch import receiver

from projects.models import Project
from .models import SDLCPhase


DEFAULT_PHASES = [
    ("requirement", 1),
    ("design", 2),
    ("development", 3),
    ("testing", 4),
    ("deployment", 5),
    ("maintenance", 6),
]


@receiver(post_save, sender=Project)
def create_default_sdlc_phases(sender, instance, created, **kwargs):

    if created:

        for phase_name, order in DEFAULT_PHASES:

            SDLCPhase.objects.create(
                project=instance,
                phase_name=phase_name,
                order=order,
                status="not_started",
                progress=0,
            )