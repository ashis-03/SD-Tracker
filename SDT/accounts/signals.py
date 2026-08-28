from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


# Automatically create Profile when a new User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)


# When a user's role changes from manager to another role
@receiver(post_save, sender=Profile)
def remove_manager_assignments(sender, instance, **kwargs):

    if instance.role != "manager":

        # Import here to avoid circular import issues
        from employees.models import Employee, Team
        from projects.models import Project

        try:
            employee = instance.user.employee

            # Remove employee as Team Manager
            Team.objects.filter(
                manager=employee
            ).update(
                manager=None
            )

            # Remove employee as Project Manager
            Project.objects.filter(
                manager=employee
            ).update(
                manager=None
            )

        except Employee.DoesNotExist:
            pass