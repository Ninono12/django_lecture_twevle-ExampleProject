from django.urls import path
from blog.views import (
    home_view,
    blog_list,
    blog_detail,
    not_found,
    real_blog_list,
    real_blog_detail
)

urlpatterns = [
    path('home/', home_view, name='home'),
    path('blogs/', blog_list, name='blog_list'),
    path("blogs/<int:post_id>/", blog_detail, name="blog_detail"),
    path('not_fount/', not_found, name='not_found'),
    path('real_blog_list/', real_blog_list, name='real_blog_list'),
    path('real_blog_detail/<int:post_id>/', real_blog_detail, name='real_blog_detail')
]
