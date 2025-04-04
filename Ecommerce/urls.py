from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
    path("blog/", views.blog, name="blog"),
    path("blog_detail/", views.blog_detail, name="blog-detail"),
    path("shop/", views.shop, name="shop"),
    path("produit/", views.produit, name="produit"),
    path("about/", views.about, name="about"),
]
