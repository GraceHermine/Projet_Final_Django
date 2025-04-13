from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("blog/", views.blog, name="blog"),
    path("blog/blog_detail/<int:blog_id>/", views.blog_detail, name="blog-detail"),

]