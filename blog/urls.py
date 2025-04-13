from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog-detail"),
    path('soumettre-article/', views.soumettre_article, name='soumettre_article'),
    path('mes-articles/', views.mes_articles, name='mes_articles'),

    # GESTION DES ARTICLES DU BLOG
    path('articles-en-attente/', views.articles_en_attente, name='articles_en_attente'),
    path('valider-article/<slug:slug>/', views.valider_article, name='valider_article'),
    path("ajouter-article/", views.ajouter_article, name='ajouter_article'),
    path("mes-articles/", views.mes_articles, name='mes_articles'),
    path("modifier-article/<int:article_id>/", views.modifier_article, name='modifier_article'),
    path("supprimer-article/<int:article_id>/", views.supprimer_article, name='supprimer_article'),

]