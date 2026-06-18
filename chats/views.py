from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Message


# ----------------------------
# CHAT ROOM
# ----------------------------
@login_required
def chat_room(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Message.objects.create(
                sender=request.user, receiver=other_user, content=content
            )

        return redirect("chat_room", user_id=other_user.id)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user], receiver__in=[request.user, other_user]
    ).order_by("timestamp")

    return render(
        request,
        "chats/chat_room.html",
        {
            "other_user": other_user,
            "messages": messages,
        },
    )


# ----------------------------
# DELETE MESSAGE (ONLY OWNER)
# ----------------------------
@login_required
@require_POST
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.sender != request.user:
        return JsonResponse({"error": "Not allowed"}, status=403)

    message.delete()

    return JsonResponse({"id": message_id})


# ----------------------------
# EDIT MESSAGE (ONLY OWNER)
# ----------------------------
@login_required
@require_POST
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.sender != request.user:
        return JsonResponse({"error": "Not allowed"}, status=403)

    new_content = request.POST.get("content")

    message.content = new_content
    message.edited = True  # ✅ THIS IS KEY
    message.save()

    return JsonResponse(
        {"id": message.id, "content": message.content, "edited": message.edited}
    )


from django.db.models import Q
from django.utils import timezone


# ----------------------------
# INBOX
# ----------------------------
@login_required
def inbox(request):
    users = User.objects.exclude(id=request.user.id)

    inbox_users = []
    for u in users:
        last_message = (
            Message.objects.filter(
                (Q(sender=request.user) & Q(receiver=u))
                | (Q(sender=u) & Q(receiver=request.user))
            )
            .order_by("-timestamp")
            .first()
        )

        inbox_users.append({"user": u, "last_message": last_message})

    # Sort by recent message first, users with no messages at the bottom
    inbox_users.sort(
        key=lambda x: (
            x["last_message"].timestamp
            if x["last_message"]
            else timezone.now().replace(year=1970)
        ),
        reverse=True,
    )

    return render(request, "chats/inbox.html", {"inbox_users": inbox_users})


# ----------------------------
# FETCH MESSAGES (AJAX)
# ----------------------------
@login_required
def fetch_messages(request, user_id):
    other_user = User.objects.get(id=user_id)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user], receiver__in=[request.user, other_user]
    ).order_by("timestamp")

    data = [
        {
            "id": m.id,
            "sender": m.sender.username,
            "content": m.content,
            "time": m.timestamp.strftime("%H:%M"),
            # ✅ ADD THIS LINE
            "edited": m.edited,
        }
        for m in messages
    ]

    return JsonResponse(data, safe=False)
