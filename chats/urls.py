from django.urls import path
from . import views

urlpatterns = [
    path("", views.inbox, name="chat_inbox"),
    path("<int:user_id>/", views.chat_room, name="chat_room"),
    path("messages/<int:user_id>/", views.fetch_messages, name="fetch_messages"),

    # NEW
    path("delete/<int:message_id>/", views.delete_message, name="delete_message"),
    path("edit/<int:message_id>/", views.edit_message, name="edit_message"),
]