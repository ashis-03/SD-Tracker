from django.urls import path
from . import views

urlpatterns = [
    path('sdlc_list/', views.sdlc_list, name='sdlc_list'),
    path('sdlc_detail/<int:pk>/', views.sdlc_detail, name='sdlc_detail'),
    path("phase/<int:pk>/status/", views.phase_status_update, name="phase_status_update"),
]