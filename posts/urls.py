from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_post, name="create_post"),
    path("api/<int:post_id>/", views.post_api, name="post_api"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),
]
