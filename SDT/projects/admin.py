from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "client_name",
        "manager",
        "status",
        "start_date",
        "deadline",
        "get_teams",
    ]

    list_filter = [
        "status",
    ]

    search_fields = [
        "name",
        "client_name",
    ]

    filter_horizontal = [
        "teams"
    ]

    @admin.display(description="Teams")
    def get_teams(self, obj):
        return ", ".join(
            team.name
            for team in obj.teams.all()
        )