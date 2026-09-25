from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from projects.models import Project

from .models import Task
from .forms import (
    TaskForm,
    TaskEditForm,
    TaskUpdateForm,
    TaskSubmissionForm,
)
from django.utils import timezone


# helper functions for checking role
def is_admin_or_manager(user):

    if user.is_superuser:
        return True

    return user.profile.role in ["admin", "manager"]


def is_task_employee(request, task):

    try:
        return task.assigned_to == request.user.employee
    except:
        return False


# task list
def task_list(request):

    tasks = Task.objects.all()

    search = request.GET.get("search")
    project_id = request.GET.get("project")
    status = request.GET.get("status")
    priority = request.GET.get("priority")

    if search:

        tasks = tasks.filter(
            title__icontains=search
        )

    if project_id:

        tasks = tasks.filter(
            project_id=project_id
        )

    if status:

        tasks = tasks.filter(
            status=status
        )

    if priority:

        tasks = tasks.filter(
            priority=priority
        )

    context = {

        "tasks": tasks,

        "projects": Project.objects.all(),

        "total_tasks": tasks.count(),

        "todo_tasks": tasks.filter(
            status="todo"
        ).count(),

        "in_progress_tasks": tasks.filter(
            status="in_progress"
        ).count(),

        "review_tasks": tasks.filter(
            status="in_review"
        ).count(),

        "completed_tasks": tasks.filter(
            status="completed"
        ).count(),
    }

    return render(
        request,
        "tasks/task_list.html",
        context
    )


# create task
def task_create(request):

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)

            task.status = "todo"
            task.progress = 0

            task.save()

            return redirect("task_list")

    else:

        form = TaskForm()

    return render(
        request,
        "tasks/task_form.html",
        {
            "form": form,
            "title": "Create Task"
        }
    )


# task details
def task_detail(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk
    )

    role = request.user.profile.role

    if role == "employee":

        back_url = "my_tasks"
        back_text = "Back to My Tasks"

    else:

        back_url = "task_list"
        back_text = "Back to Tasks"

    return render(
        request,
        "tasks/task_detail.html",
        {
            "task": task,
            "back_url": back_url,
            "back_text": back_text,
        }
    )


# Edit option 
def task_edit(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk
    )

    if not is_admin_or_manager(request.user):
        return HttpResponseForbidden(
            "You do not have permission to edit this task."
        )

    if request.method == "POST":

        form = TaskEditForm(
            request.POST,
            instance=task
        )

        if form.is_valid():

            form.save()

            return redirect(
                "task_detail",
                pk=task.pk
            )

    else:

        form = TaskEditForm(
            instance=task
        )

    return render(
        request,
        "tasks/task_edit.html",
        {
            "form": form,
            "task": task,
            "title": "Edit Task"
        }
    )

# for individual employees 
def my_tasks(request):

    employee = request.user.employee

    tasks = Task.objects.filter(
        assigned_to=employee
    )

    context = {
        "tasks": tasks,

        "total_tasks": tasks.count(),

        "todo_tasks": tasks.filter(
            status="todo"
        ).count(),

        "in_progress_tasks": tasks.filter(
            status="in_progress"
        ).count(),

        "completed_tasks": tasks.filter(
            status="completed"
        ).count(),
    }

    return render(
        request,
        "tasks/my_tasks.html",
        context
    )

# for employees
def task_progress(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk
    )

    # Only assigned employee can update progress
    if not is_task_employee(request, task):
        return HttpResponseForbidden(
            "You do not have permission to update this task."
        )

    if request.method == "POST":

        form = TaskUpdateForm(
            request.POST,
            instance=task
        )

        if form.is_valid():

            task = form.save(commit=False)

            # Automatically start task
            if task.status == "todo" and task.progress > 0:

                task.status = "in_progress"

            task.save()

            return redirect(
                "task_detail",
                pk=task.pk
            )

    else:

        form = TaskUpdateForm(
            instance=task
        )

    return render(
        request,
        "tasks/task_progress.html",
        {
            "form": form,
            "task": task,
            "title": "Update Progress"
        }
    )


# for employee
def submit_task(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk
    )

    # Only assigned employee
    if not is_task_employee(request, task):
        return HttpResponseForbidden(
            "You do not have permission to submit this task."
        )

    if request.method == "POST":

        form = TaskSubmissionForm(
            request.POST,
            request.FILES,
            instance=task
        )

        if form.is_valid():

            task = form.save(commit=False)

            task.status = "in_review"

            task.review_status = "pending"

            task.submitted_at = timezone.now()

            task.save()

            return redirect(
                "task_detail",
                pk=task.pk
            )

    else:

        form = TaskSubmissionForm(
            instance=task
        )

    return render(
        request,
        "tasks/task_submit.html",
        {
            "form": form,
            "task": task
        }
    )


# review task
def review_task(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk
    )

    if not is_admin_or_manager(request.user):
        return HttpResponseForbidden(
            "You do not have permission to review this task."
        )

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "approve":

            task.review_status = "approved"
            task.status = "completed"
            task.progress = 100

        elif action == "changes":

            task.review_status = "changes_requested"
            task.status = "in_progress"

        elif action == "reject":

            task.review_status = "rejected"

        task.save()

    return redirect(
        "task_detail",
        pk=task.pk
    ) 


# Add Manager/Admin review views
def approve_task(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk
    )

    if request.method == "POST":

        task.review_status = "approved"

        task.status = "completed"

        task.progress = 100

        task.save()

    return redirect(
        "task_detail",
        pk=task.pk
    )


# Request Changes
def request_changes(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk
    )

    if request.method == "POST":

        task.review_status = "changes_requested"

        task.status = "in_progress"

        task.save()

    return redirect(
        "task_detail",
        pk=task.pk
    )

# Reject
def reject_task(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk
    )

    if request.method == "POST":

        task.review_status = "rejected"

        task.save()

    return redirect(
        "task_detail",
        pk=task.pk
    )