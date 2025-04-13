from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
  
    path("about/", views.about, name="about"),
    path("service/", views.service, name="service"),
    path('faq/', views.faq, name='faq'),
    path("notfound/", views.notfound, name="notfound"),
    path("policy/", views.policy, name="policy"),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
]
