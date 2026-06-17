from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import StudentProfile   # ✅ correct model
from posts.models import Post
from chats.models import Message
from django.db.models import Count
import random
import string


@never_cache
@login_required
def dashboard_home(request):
    posts = Post.objects.all().order_by("-created_at")

    return render(request, "dashboard/dashboard.html", {"posts": posts})


def admin_panel(request):
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()

    total_programs = StudentProfile.objects.values("program").distinct().count()

    total_posts = Post.objects.count()
    recent_posts = Post.objects.select_related('user').all().order_by("-created_at")[:5]
    
    total_messages = Message.objects.count()
    
    completed_profiles = StudentProfile.objects.filter(profile_completed=True).count()
    profile_completion_rate = 0
    if total_users > 0:
        profile_completion_rate = int((completed_profiles / total_users) * 100)
        
    recent_users = User.objects.filter(is_staff=False).order_by("-date_joined")[:5]
    
    programs_breakdown = StudentProfile.objects.exclude(program__isnull=True).exclude(program="").values("program").annotate(count=Count("id")).order_by("-count")[:5]

    context = {
        "total_users": total_users,
        "active_users": active_users,
        "staff_users": staff_users,
        "total_programs": total_programs,
        "total_posts": total_posts,
        "recent_posts": recent_posts,
        "total_messages": total_messages,
        "profile_completion_rate": profile_completion_rate,
        "recent_users": recent_users,
        "programs_breakdown": programs_breakdown,
    }

    return render(request, "dashboard/admin.html", context)


def manage_users(request):
    search = request.GET.get("search")

    if search:
        users = User.objects.filter(is_staff=False, username__icontains=search)
    else:
        users = User.objects.filter(is_staff=False)

    for user in users:
        StudentProfile.objects.get_or_create(user=user)  # ✅ FIXED

    return render(request, "dashboard/manage_users.html", {"users": users})


def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()

    messages.success(request, "User deleted successfully")
    return redirect("/admin-panel/manage/")


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    profile, created = StudentProfile.objects.get_or_create(user=user)  # ✅ FIXED

    if request.method == "POST":
        user.email = request.POST["email"]
        user.save()

        profile.save()

        messages.success(request, "User updated successfully")
        return redirect("/admin-panel/manage/")

    return render(request, "dashboard/edit_user.html", {
        "user": user,
        "profile": profile
    })


def reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)

    chars = string.ascii_letters + string.digits
    temp_password = "".join(random.choice(chars) for _ in range(8))

    user.set_password(temp_password)
    user.save()

    messages.success(
        request,
        f"{user.email}'s password reset. New password: {temp_password}"
    )

    return redirect("manage_users")