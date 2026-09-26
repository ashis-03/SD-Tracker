from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from projects.models import Project
from tasks.models import Task
from employees.models import Employee, Team
from sdlc.models import SDLCPhase


# =========================================================
# COMMON DASHBOARD DATA
# =========================================================

def get_project_data(projects):
    """
    Return project progress information for dashboard cards.
    """

    project_progress = []

    for project in projects:
        project_progress.append({
            "project": project,
            "progress": project.progress,
        })

    return project_progress


def get_upcoming_deadlines(projects, tasks):
    """
    Collect upcoming project/task deadlines.
    """

    today = timezone.now().date()

    deadlines = []

    # Project deadlines
    for project in projects:
        if project.deadline and project.deadline >= today:
            deadlines.append({
                "name": project.name,
                "type": "Project deadline",
                "date": project.deadline,
            })

    # Task deadlines
    for task in tasks:
        if task.deadline and task.deadline >= today:
            deadlines.append({
                "name": task.title,
                "type": "Task deadline",
                "date": task.deadline,
            })

    deadlines.sort(key=lambda x: x["date"])

    return deadlines[:5]


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    user = request.user
    role = user.profile.role

    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    if role == "admin":

        projects = Project.objects.all().select_related(
            "manager__user"
        )

        tasks = Task.objects.all().select_related(
            "project",
            "assigned_to__user",
            "phase",
        )

        phases = SDLCPhase.objects.all()

        employees = Employee.objects.all()

        teams = Team.objects.all()

        # -------------------------------------------------
        # PROJECT STATISTICS
        # -------------------------------------------------

        total_projects = projects.count()

        active_projects = projects.filter(
            status="active"
        ).count()

        completed_projects = projects.filter(
            status="completed"
        ).count()

        planning_projects = projects.filter(
            status="planning"
        ).count()

        on_hold_projects = projects.filter(
            status="on_hold"
        ).count()

        # -------------------------------------------------
        # TASK STATISTICS
        # -------------------------------------------------

        total_tasks = tasks.count()

        todo_tasks = tasks.filter(
            status="todo"
        ).count()

        in_progress_tasks = tasks.filter(
            status="in_progress"
        ).count()

        review_tasks = tasks.filter(
            status="in_review"
        ).count()

        completed_tasks = tasks.filter(
            status="completed"
        ).count()

        today = timezone.now().date()

        overdue_tasks = tasks.filter(
            deadline__lt=today
        ).exclude(
            status="completed"
        ).count()

        # -------------------------------------------------
        # SDLC STATISTICS
        # -------------------------------------------------

        total_phases = phases.count()

        planning_phases = phases.filter(
            status="not_started"
        ).count()

        active_phases = phases.filter(
            status="in_progress"
        ).count()

        on_hold_phases = phases.filter(
            status="on_hold"
        ).count()

        completed_phases = phases.filter(
            status="completed"
        ).count()

        # -------------------------------------------------
        # PROJECT PROGRESS
        # -------------------------------------------------

        project_progress = get_project_data(projects)

        # -------------------------------------------------
        # RECENT PROJECTS
        # -------------------------------------------------

        recent_projects = projects.order_by(
            "-id"
        )[:5]

        # -------------------------------------------------
        # RECENT TASKS
        # -------------------------------------------------

        recent_tasks = tasks.order_by(
            "-created_at"
        )[:5]

        # -------------------------------------------------
        # UPCOMING DEADLINES
        # -------------------------------------------------

        upcoming_deadlines = get_upcoming_deadlines(
            projects,
            tasks
        )

        # -------------------------------------------------
        # CONTEXT
        # -------------------------------------------------

        context = {

            # User
            "dashboard_role": "admin",

            # Projects
            "total_projects": total_projects,
            "active_projects": active_projects,
            "completed_projects": completed_projects,
            "planning_projects": planning_projects,
            "on_hold_projects": on_hold_projects,

            # Tasks
            "total_tasks": total_tasks,
            "todo_tasks": todo_tasks,
            "in_progress_tasks": in_progress_tasks,
            "review_tasks": review_tasks,
            "completed_tasks": completed_tasks,
            "overdue_tasks": overdue_tasks,

            # Employees / Teams
            "total_employees": employees.count(),
            "team_members": employees.count(),
            "total_teams": teams.count(),

            # SDLC
            "total_phases": total_phases,
            "planning_phases": planning_phases,
            "active_phases": active_phases,
            "on_hold_phases": on_hold_phases,
            "completed_phases": completed_phases,

            # Lists
            "project_progress": project_progress,
            "recent_projects": recent_projects,
            "recent_tasks": recent_tasks,
            "upcoming_deadlines": upcoming_deadlines,

            # Empty until Notification/Activity models exist
            "recent_activities": [],
            "unread_notifications": 0,
        }

        return render(
            request,
            "dashboard/admin_dashboard.html",
            context
        )

    # =====================================================
    # MANAGER DASHBOARD
    # =====================================================

    elif role == "manager":

        employee = user.employee

        # -------------------------------------------------
        # MANAGER'S PROJECTS
        # -------------------------------------------------

        projects = Project.objects.filter(
            manager=employee
        ).select_related(
            "manager__user"
        ).distinct()


        # -------------------------------------------------
        # TASKS BELONGING TO MANAGER'S PROJECTS
        # -------------------------------------------------

        tasks = Task.objects.filter(
            project__in=projects
        ).select_related(
            "project",
            "assigned_to__user",
            "phase",
        )


        # -------------------------------------------------
        # PHASES BELONGING TO MANAGER'S PROJECTS
        # -------------------------------------------------

        phases = SDLCPhase.objects.filter(
            project__in=projects
        )


        # -------------------------------------------------
        # TEAMS CONNECTED TO MANAGER'S PROJECTS
        # -------------------------------------------------

        teams = Team.objects.filter(
            projects__in=projects
        ).distinct()


        # -------------------------------------------------
        # TEAM MEMBERS
        # -------------------------------------------------

        team_members = Employee.objects.filter(
            teams__in=teams
        ).select_related(
            "user",
            "user__profile"
        ).distinct()

        # Number of team members
        total_team_members = team_members.count()


        today = timezone.now().date()


        # =================================================
        # PROJECT STATISTICS
        # =================================================

        total_projects = projects.count()

        active_projects = projects.filter(
            status="active"
        ).count()

        completed_projects = projects.filter(
            status="completed"
        ).count()

        planning_projects = projects.filter(
            status="planning"
        ).count()

        on_hold_projects = projects.filter(
            status="on_hold"
        ).count()


        # =================================================
        # TASK STATISTICS
        # =================================================

        total_tasks = tasks.count()

        todo_tasks = tasks.filter(
            status="todo"
        ).count()

        in_progress_tasks = tasks.filter(
            status="in_progress"
        ).count()

        review_tasks = tasks.filter(
            status="in_review"
        ).count()

        completed_tasks = tasks.filter(
            status="completed"
        ).count()

        overdue_tasks = tasks.filter(
            deadline__lt=today
        ).exclude(
            status="completed"
        ).count()


        # =================================================
        # SDLC STATISTICS
        # =================================================

        total_phases = phases.count()

        active_phases = phases.filter(
            status="in_progress"
        ).count()

        completed_phases = phases.filter(
            status="completed"
        ).count()

        on_hold_phases = phases.filter(
            status="on_hold"
        ).count()


        # =================================================
        # CONTEXT
        # =================================================

        context = {

            "dashboard_role": "manager",

            # -------------------------------------------------
            # USER
            # -------------------------------------------------

            "current_employee": employee,


            # -------------------------------------------------
            # PROJECTS
            # -------------------------------------------------

            "total_projects": total_projects,
            "active_projects": active_projects,
            "completed_projects": completed_projects,
            "planning_projects": planning_projects,
            "on_hold_projects": on_hold_projects,


            # -------------------------------------------------
            # TASKS
            # -------------------------------------------------

            "total_tasks": total_tasks,
            "todo_tasks": todo_tasks,
            "in_progress_tasks": in_progress_tasks,
            "review_tasks": review_tasks,
            "completed_tasks": completed_tasks,
            "overdue_tasks": overdue_tasks,


            # -------------------------------------------------
            # TEAMS
            # -------------------------------------------------

            # IMPORTANT:
            # Keep the queryset here because the template
            # loops through team_members.

            "team_members": team_members,

            # Number used for the statistics card

            "total_team_members": total_team_members,

            "teams": teams,


            # -------------------------------------------------
            # SDLC
            # -------------------------------------------------

            "total_phases": total_phases,
            "active_phases": active_phases,
            "completed_phases": completed_phases,
            "on_hold_phases": on_hold_phases,


            # -------------------------------------------------
            # LISTS
            # -------------------------------------------------

            "project_progress": get_project_data(
                projects
            ),

            "recent_projects": projects.order_by(
                "-id"
            )[:5],

            "recent_tasks": tasks.order_by(
                "-created_at"
            )[:5],

            "upcoming_deadlines": get_upcoming_deadlines(
                projects,
                tasks
            ),


            # -------------------------------------------------
            # RECENT TEAM MEMBERS
            # -------------------------------------------------

            "recent_team_members": team_members[:5],


            # -------------------------------------------------
            # NOT IMPLEMENTED YET
            # -------------------------------------------------

            "recent_activities": [],

            "unread_notifications": 0,
        }


        return render(
            request,
            "dashboard/manager_dashboard.html",
            context
        )

    # =====================================================
    # EMPLOYEE DASHBOARD
    # =====================================================

    elif role == "employee":

        employee = user.employee

        # Employee's assigned tasks
        tasks = Task.objects.filter(
            assigned_to=employee
        ).select_related(
            "project",
            "phase",
            "assigned_to__user",
        )

        # Employee's projects
        projects = Project.objects.filter(
            tasks__assigned_to=employee
        ).select_related(
            "manager__user"
        ).distinct()

        # Employee's phases
        phases = SDLCPhase.objects.filter(
            tasks__assigned_to=employee
        ).distinct()

        today = timezone.now().date()

        # -------------------------------------------------
        # TASK STATISTICS
        # -------------------------------------------------

        total_tasks = tasks.count()

        todo_tasks = tasks.filter(
            status="todo"
        ).count()

        in_progress_tasks = tasks.filter(
            status="in_progress"
        ).count()

        review_tasks = tasks.filter(
            status="in_review"
        ).count()

        completed_tasks = tasks.filter(
            status="completed"
        ).count()

        overdue_tasks = tasks.filter(
            deadline__lt=today
        ).exclude(
            status="completed"
        ).count()

        # -------------------------------------------------
        # PROJECT STATISTICS
        # -------------------------------------------------

        total_projects = projects.count()

        active_projects = projects.filter(
            status="active"
        ).count()

        completed_projects = projects.filter(
            status="completed"
        ).count()

        # -------------------------------------------------
        # SDLC PHASES
        # -------------------------------------------------

        active_phases = phases.filter(
            status="in_progress"
        ).count()

        completed_phases = phases.filter(
            status="completed"
        ).count()

        # -------------------------------------------------
        # SUBMISSIONS
        # -------------------------------------------------

        submissions = tasks.exclude(
            work_file=""
        ).exclude(
            work_file=None
        )

        total_submissions = submissions.count()

        # -------------------------------------------------
        # CONTEXT
        # -------------------------------------------------

        context = {

            "dashboard_role": "employee",

            # User
            "current_employee": employee,

            # Tasks
            "total_tasks": total_tasks,
            "my_tasks": total_tasks,
            "todo_tasks": todo_tasks,
            "in_progress_tasks": in_progress_tasks,
            "review_tasks": review_tasks,
            "completed_tasks": completed_tasks,
            "overdue_tasks": overdue_tasks,

            # Projects
            "total_projects": total_projects,
            "my_projects": total_projects,
            "active_projects": active_projects,
            "completed_projects": completed_projects,

            # SDLC
            "active_phases": active_phases,
            "completed_phases": completed_phases,

            # Submissions
            "total_submissions": total_submissions,
            "my_submissions": total_submissions,

            # Lists
            "project_progress": get_project_data(projects),
            "assigned_projects": projects[:5],
            "recent_tasks": tasks.order_by("-created_at")[:5],
            "upcoming_deadlines": get_upcoming_deadlines(
                projects,
                tasks
            ),

            # Notification model has not been provided
            "unread_notifications": 0,
            "recent_notifications": [],
        }

        return render(
            request,
            "dashboard/employee_dashboard.html",
            context
        )

    # =====================================================
    # FALLBACK
    # =====================================================

    return render(
        request,
        "dashboard/employee_dashboard.html",
        {
            "dashboard_role": "employee",
            "unread_notifications": 0,
        }
    )