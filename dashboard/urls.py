from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='student_dashboard'),
    path(
        'delete-user/<int:user_id>/',
        views.delete_user,
        name='delete_user'
    ),
    path(
        'edit-user/<int:user_id>/',
        views.edit_user,
        name='edit_user'
    ),
    path("reset-password/<int:user_id>/", views.reset_password, name="reset_password"),
    path(
    "student/<int:user_id>/",
    views.student_profile,
    name="student_profile"
),
]