from django.urls import path
from . import views

urlpatterns = [
    path("", views.inbox, name="chat_inbox"),
    path("<int:user_id>/", views.chat_room, name="chat_room"),
    path("messages/<int:user_id>/", views.fetch_messages, name="fetch_messages"),
]

