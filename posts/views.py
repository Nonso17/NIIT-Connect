from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post


@login_required
def create_post(request):

    if request.method == "POST":

        content = request.POST.get("content")
        link = request.POST.get("link")
        image = request.FILES.get("image")

        if content or link or image:

            Post.objects.create(user=request.user, content=content, link=link, image=image)

        return redirect("/dashboard/")

    return redirect("/dashboard/")
