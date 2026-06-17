from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .models import StudentProfile

import random
import string


# -----------------------------
# LOGIN
# -----------------------------
def login_view(request):

    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("/admin-panel/")
        return redirect("/dashboard/")

    if request.method == "POST":

        email = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("/accounts/login/")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect("/admin-panel/")

            profile, created = StudentProfile.objects.get_or_create(user=user)

            if profile.must_change_password:
                return redirect("change_password")

            if not profile.profile_completed:
                return redirect("complete_profile")

            return redirect("/dashboard/")

        messages.error(request, "Invalid email or password")
        return redirect("/accounts/login/")

    return render(request, "accounts/login.html")


# -----------------------------
# LOGOUT
# -----------------------------
def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")


# -----------------------------
# TEMP PASSWORD GENERATOR
# -----------------------------
def generate_temp_password(length=8):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


# -----------------------------
# REGISTER USER (ADMIN ONLY)
# -----------------------------
def register_view(request):

    if request.method == "POST":

        email = request.POST["email"]

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("/admin-panel/manage/")

        username = email.split("@")[0]

        if User.objects.filter(username=username).exists():
            username = username + str(random.randint(100, 999))

        temp_password = generate_temp_password()

        user = User.objects.create_user(
            username=username,
            email=email,
            password=temp_password
        )

        StudentProfile.objects.create(
            user=user,
            must_change_password=True
        )

        messages.success(
            request,
            f"User created. Temp password: {temp_password}"
        )

        return redirect("/admin-panel/manage/")

    return redirect("/admin-panel/manage/")


# -----------------------------
# PROFILE VIEW
# -----------------------------
@login_required
def profile_view(request):

    profile, created = StudentProfile.objects.get_or_create(user=request.user)

    return render(request, "accounts/profile.html", {
        "profile": profile
    })


# -----------------------------
# PROFILE API
# -----------------------------
@login_required
def profile_api(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    profile, created = StudentProfile.objects.get_or_create(user=user_obj)
    
    data = {
        "id": user_obj.id,
        "email": user_obj.email,
        "first_name": user_obj.first_name,
        "last_name": user_obj.last_name,
        "full_name": profile.full_name,
        "number": profile.number,
        "program": profile.program,
        "year": profile.year,
        "bio": profile.bio if hasattr(profile, 'bio') else "",
        "profile_picture": profile.profile_picture.url if profile.profile_picture else None,
    }
    return JsonResponse(data)


# -----------------------------
# EDIT PROFILE
# -----------------------------
@login_required
def edit_profile(request):

    profile = request.user.studentprofile

    if request.method == "POST":

        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")
        request.user.save()

        profile.full_name = request.POST.get("full_name")
        profile.number = request.POST.get("number")
        profile.program = request.POST.get("program")
        profile.year = request.POST.get("year")

        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES.get("profile_picture")

        profile.save()

        messages.success(request, "Profile updated successfully")

        return redirect("profile")

    return redirect("profile")


# -----------------------------
# CHANGE PASSWORD
# -----------------------------
@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():

            user = form.save()
            update_session_auth_hash(request, user)

            profile = request.user.studentprofile
            profile.must_change_password = False
            profile.save()

            messages.success(request, "Password changed successfully")

            return redirect("/dashboard/")

    else:
        form = PasswordChangeForm(request.user)

    return render(request, "accounts/change_password.html", {
        "form": form
    })


# -----------------------------
# COMPLETE PROFILE
# -----------------------------
@login_required
def complete_profile(request):

    profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        profile.full_name = request.POST.get("full_name")
        profile.number = request.POST.get("number")
        profile.program = request.POST.get("program")
        profile.year = request.POST.get("year")
        profile.profile_picture = request.FILES.get("profile_picture")

        profile.profile_completed = True
        profile.save()

        return redirect("/dashboard/")

    return render(request, "accounts/complete_profile.html")