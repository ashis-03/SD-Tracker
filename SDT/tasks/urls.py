from django.urls import path
from . import views


urlpatterns = [

    # Task List
    path("",views.task_list,name="task_list"),

    # Create Task
    path("create/",views.task_create,name="task_create"),

    # My Tasks
    path("my-tasks/",views.my_tasks,name="my_tasks"),

    # Task Detail
    path("<int:pk>/",views.task_detail,name="task_detail"),

    # Edit Task
    path("<int:pk>/edit/",views.task_edit,name="task_edit"),

    # Update Progress
    path("<int:pk>/progress/",views.task_progress,name="task_progress"),

    # Submit Task
    path("<int:pk>/submit/",views.submit_task,name="submit_task"),

    # Review Task 
    path("<int:pk>/review/",views.review_task,name="review_task"),

]