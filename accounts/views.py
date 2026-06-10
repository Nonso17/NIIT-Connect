from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import StudentProfile
import random
import string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


def login_view(request):

    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("/admin-panel/")
        return redirect("/dashboard/")

    if request.method == "POST":

        email = request.POST.get(
            "username"
        )  # your input is still called username in HTML
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


def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")


def generate_temp_password(length=8):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def register_view(request):

    if request.method == "POST":

        email = request.POST["email"]

        # prevent duplicate email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("/admin-panel/manage/")

        # auto username from email
        username = email.split("@")[0]

        # ensure username is unique
        if User.objects.filter(username=username).exists():
            username = username + str(random.randint(100, 999))

        temp_password = generate_temp_password()

        # create user
        user = User.objects.create_user(
            username=username, email=email, password=temp_password
        )

        # create profile
        StudentProfile.objects.create(user=user, must_change_password=True)

        messages.success(request, f"User created. Temp password: {temp_password}")

        return redirect("/admin-panel/manage/")

    return redirect("/admin-panel/manage/")


@login_required
def profile_view(request):

    profile = request.user.studentprofile

    context = {"profile": profile}

    return render(request, "accounts/profile.html", context)


@login_required
def edit_profile(request):

    profile = request.user.studentprofile

    if request.method == "POST":

        # User model fields
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")
        request.user.save()

        # StudentProfile fields
        profile.bio = request.POST.get("bio")
        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")

        # profile picture
        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES.get("profile_picture")

        profile.save()

        messages.success(request, "Profile updated successfully")

        return redirect("profile")

    context = {"profile": profile}

    return render(request, "accounts/edit_profile.html", context)


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

            return redirect("student_dashboard")

    else:

        form = PasswordChangeForm(request.user)

    context = {"form": form}

    return render(request, "accounts/change_password.html", context)


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
