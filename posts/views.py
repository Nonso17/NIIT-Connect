from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post


@login_required
def create_post(request):

    if request.method == "POST":

        content = request.POST.get("content")

        if content:

            Post.objects.create(user=request.user, content=content)

        return redirect("/dashboard/")

    return redirect("/dashboard/")
