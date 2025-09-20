from django.urls import path
from .views import blog_detail, blog_list, not_found, real_blog_list, real_blog_detail
urlpatterns = [
    path("blogs/", blog_list, name="blog_list"),
    path('blogs/<int:blog_id>', blog_detail, name='blog_detail'),
    path('not_found/', not_found, name='not_found'),
    path('real_blogs/', real_blog_list, name='real_blog_list'),
    path('real_blogs/<int:blog_id>', real_blog_detail, name='real_blog_detail'),
]
