from django.shortcuts import render, redirect
from django.urls import reverse

from blog.models import BlogPost


def home_view(request):
    return render(request, "home.html", {
        "title": "Home Page",
        "description": "Welcome to my blog! Here you'll find the latest posts."
    })

blogs = [
    {
        "id": 1,
        "title": "First Blog Post",
        "author": "Alice",
        "date": "2025-09-01",
        "content": "This is the first blog post content..."
    },
    {
        "id": 2,
        "title": "Second Blog Post",
        "author": "Bob",
        "date": "2025-09-05",
        "content": "This is the second blog post content..."
    },
    {
        "id": 3,
        "title": "Third Blog Post",
        "author": "Charlie",
        "date": "2025-09-08",
        "content": "Another exciting update..."
    },
]

def blog_list(request):
    return render(request, "blog.html", {
        "title": "All Blog Posts",
        "blogs": blogs,
    })


def blog_detail(request, post_id):
    blog = next((b for b in blogs if b["id"] == post_id), None)
    if not blog:
        return redirect(reverse('not_found'))

    return render(request, "blog_detail.html", {
        "title": blog["title"],
        "blog": blog,
    })


def not_found(request):
    return render(request, "404.html", {})


def real_blog_list(request):
    return render(request, context={
        'title': 'Real Blog Post',
        'blog_posts': BlogPost.objects.all(),
    }, template_name="real_blog_post.html")


def real_blog_detail(request, post_id):
    blog_post = BlogPost.objects.filter(id=post_id).first()
    if not blog_post:
        return redirect(reverse('not_found'))


    return render(request, "real_blog_detail.html", {
        "title": blog_post.title,
        "blog": blog_post
    })