from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden


@login_required
def create_post(request):

    if request.method == "POST":

        content = request.POST.get("content")
        link = request.POST.get("link")
        image = request.FILES.get("image")

        if content or link or image:

            Post.objects.create(
                user=request.user, content=content, link=link, image=image
            )

        return redirect("/dashboard/")

    return redirect("/dashboard/")


@login_required
def post_api(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    data = {
        "id": post.id,
        "user_id": post.user.id,
        "content": post.content or "",
        "image": post.image.url if post.image else None,
        "link": post.link or "",
        "created_at": post.created_at.strftime("%b %d, %Y at %I:%M %p"),
    }
    return JsonResponse(data)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        content = request.POST.get("content")
        link = request.POST.get("link")
        image = request.FILES.get("image")

        post.content = content
        post.link = link
        if image:
            post.image = image
        post.save()

        return JsonResponse({"success": True, "post": {
            "id": post.id,
            "content": post.content or "",
            "image": post.image.url if post.image else None,
            "link": post.link or "",
        }})

    return JsonResponse({"error": "Invalid method"}, status=400)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        post.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid method"}, status=400)
