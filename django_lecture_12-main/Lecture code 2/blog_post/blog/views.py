from django.shortcuts import render, redirect
from django.urls import reverse

from blog.models import BlogPost

# Demo data
BLOGS = [
    {"id": 1, "title": "Getting Started with Django", "content": "Django makes it easier to build better web apps more quickly and with less code."},
    {"id": 2, "title": "Understanding Templates", "content": "Templates let you separate the design of your Django app from the Python code."},
    {"id": 3, "title": "Deploying Your App", "content": "When your project is ready, you can deploy it to production using a variety of methods."},
]


def blog_list(request):
    return render(request, "blog_list.html", {"blogs": BLOGS})


def blog_detail(request, blog_id):
    # find the blog with matching id or return 404
    blog = next((b for b in BLOGS if b["id"] == blog_id), None)
    if not blog:
        return redirect(reverse('not_found'))

    return render(request, "blog_detail.html", {"blog": blog})


def not_found(request):
    return render(request, "404.html", status=404)


def real_blog_list(request):
    blogs = BlogPost.objects.all()
    return render(request, "real_blog_list.html", {"blogs": blogs})


def real_blog_detail(request, blog_id):
    blog = BlogPost.objects.filter(id=blog_id).first()
    if not blog:
        return redirect(reverse('not_found'))

    return render(request, "real_blog_detail.html", {"blog": blog})