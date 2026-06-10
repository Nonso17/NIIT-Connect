from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message

@login_required
def chat_room(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        content = request.POST.get("content")

        Message.objects.create(
            sender=request.user,
            receiver=other_user,
            content=content
        )

        return redirect("chat_room", user_id=other_user.id)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("timestamp")

    return render(request, "chats/chat_room.html", {
        "other_user": other_user,
        "messages": messages
    })

@login_required
def inbox(request):
    users = User.objects.exclude(id=request.user.id)

    context = {
        "users": users
    }

    return render(request, "chats/inbox.html", context)