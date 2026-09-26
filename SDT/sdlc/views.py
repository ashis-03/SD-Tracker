from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from projects.models import Project
from employees.models import Employee, Team
from .models import SDLCPhase


# =========================================================
# SDLC LIST
# =========================================================

@login_required
def sdlc_list(request):

    projects = Project.objects.prefetch_related(
        "phases",
        "teams__members__user",
    ).select_related(
        "manager__user"
    )

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    team_id = request.GET.get("team", "").strip()

    # Search
    if search:
        projects = projects.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(client_name__icontains=search)
        )

    # Project status filter
    if status:
        projects = projects.filter(status=status)

    # Team filter
    if team_id:
        projects = projects.filter(
            teams__id=team_id
        )

    projects = projects.distinct()

    # Admin → all teams
    if request.user.profile.role == "admin":
        teams = Team.objects.all()

    # Manager → teams connected to manager's projects
    elif request.user.profile.role == "manager":
        teams = Team.objects.filter(
            projects__manager=request.user.employee
        ).distinct()

    else:
        teams = request.user.employee.teams.all().distinct()

    context = {
        "projects": projects,
        "teams": teams,

        "total_projects": Project.objects.count(),
        "planning_projects": Project.objects.filter(
            status="planning"
        ).count(),
        "active_projects": Project.objects.filter(
            status="active"
        ).count(),
        "on_hold_projects": Project.objects.filter(
            status="on_hold"
        ).count(),
        "completed_projects": Project.objects.filter(
            status="completed"
        ).count(),

        "search": search,
        "selected_status": status,
        "selected_team": team_id,
    }

    return render(
        request,
        "sdlc/sdlc_list.html",
        context
    )


# =========================================================
# SDLC DETAIL
# =========================================================

@login_required
def sdlc_detail(request, pk):

    project = get_object_or_404(
        Project.objects.select_related(
            "manager__user"
        ).prefetch_related(
            "phases__tasks__assigned_to__user",
            "teams__members__user",
        ),
        pk=pk
    )

    phases = project.phases.all()

    # All employees belonging to project's teams
    project_members = Employee.objects.filter(
        teams__projects=project
    ).select_related(
        "user"
    ).distinct()

    active_phase = phases.filter(
        status="in_progress"
    ).first()

    if not active_phase:
        active_phase = phases.exclude(
            status="completed"
        ).first()

    context = {
        "project": project,
        "phases": phases,
        "project_members": project_members,

        "active_phase": active_phase,

        # Send status choices to template
        "status_choices": SDLCPhase.STATUS_CHOICES,

        "total_phases": phases.count(),

        "completed_phases": phases.filter(
            status="completed"
        ).count(),

        "in_progress_phases": phases.filter(
            status="in_progress"
        ).count(),

        "on_hold_phases": phases.filter(
            status="on_hold"
        ).count(),

        "overall_progress": project.progress,
    }

    return render(
        request,
        "sdlc/sdlc_detail.html",
        context
    )


# =========================================================
# PHASE STATUS UPDATE
# =========================================================

@login_required
def phase_status_update(request, pk):

    phase = get_object_or_404(
        SDLCPhase.objects.select_related("project"),
        pk=pk
    )

    # Only Admin and Manager
    if request.user.profile.role not in ["admin", "manager"]:
        raise PermissionDenied

    # Manager can only control their own projects
    if request.user.profile.role == "manager":

        if phase.project.manager != request.user.employee:
            raise PermissionDenied

    if request.method == "POST":

        new_status = request.POST.get("status")

        valid_statuses = dict(
            SDLCPhase.STATUS_CHOICES
        )

        if new_status in valid_statuses:

            phase.status = new_status
            phase.save(
                update_fields=["status"]
            )

    return redirect(
        "sdlc_detail",
        pk=phase.project.pk
    )    