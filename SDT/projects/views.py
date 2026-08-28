from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Project
from .forms import ProjectForm


# project list
def project_list(request):

    projects = Project.objects.all()

    search_query = request.GET.get("search")

    if search_query:

        projects = projects.filter(
            Q(name__icontains=search_query) |
            Q(client_name__icontains=search_query)
        )

    status = request.GET.get("status")

    if status:

        projects = projects.filter(
            status=status
        )

    total_projects = Project.objects.count()

    active_projects = Project.objects.filter(
        status="active"
    ).count()

    completed_projects = Project.objects.filter(
        status="completed"
    ).count()

    on_hold_projects = Project.objects.filter(
        status="on_hold"
    ).count()

    context = {

        "projects": projects,

        "total_projects": total_projects,

        "active_projects": active_projects,

        "completed_projects": completed_projects,

        "on_hold_projects": on_hold_projects,

        "status_choices": Project.STATUS_CHOICES,
    }

    return render(
        request,
        "projects/project_list.html",
        context
    )


# project create
def project_create(request):

    if request.method == "POST":

        form = ProjectForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("project_list")

    else:

        form = ProjectForm()

    return render(
        request,
        "projects/project_form.html",
        {
            "form": form,
            "title": "Create Project"
        }
    )


# project details
def project_detail(request, pk):

    project = get_object_or_404(
        Project,
        pk=pk
    )

    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project
        }
    )


# Edit
def project_edit(request, pk):

    project = get_object_or_404(
        Project,
        pk=pk
    )

    if request.method == "POST":

        form = ProjectForm(
            request.POST,
            instance=project
        )

        if form.is_valid():

            form.save()

            return redirect(
                "project_detail",
                pk=project.pk
            )

    else:

        form = ProjectForm(
            instance=project
        )

    return render(
        request,
        "projects/project_form.html",
        {
            "form": form,
            "title": "Edit Project"
        }
    )


# delete form
def project_delete(request, pk):

    project = get_object_or_404(
        Project,
        pk=pk
    )

    if request.method == "POST":

        project.delete()

        return redirect("project_list")

    return render(
        request,
        "projects/project_confirm_delete.html",
        {
            "project": project
        }
    )