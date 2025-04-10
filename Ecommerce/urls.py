from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
    path("blog/", views.blog, name="blog"),
    path("blog/blog_detail/<int:blog_id>/", views.blog_detail, name="blog-detail"),
    path("shop/", views.shop, name="shop"),
    path("produit/<int:produit_id>/", views.produit, name="produit"),
    path("about/", views.about, name="about"),
    path("service/", views.service, name="service"),
    path("account/", views.account, name="account"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("policy/", views.policy, name="policy"),
    
    path("notfound/", views.notfound, name="notfound"),
    path("checkout/", views.checkout, name="checkout"),
    path("cart/", views.cart, name="cart"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path('profile/', views.profile, name='profile'),
    path('faq/', views.faq, name='faq'),
    path('favoris/ajouter/<int:produit_id>/', views.ajouter_favoris, name='ajouter_favoris'),
    path('favoris/supprimer/<int:produit_id>/', views.supprimer_favoris, name='supprimer_favoris'),
    path('ajouter-au-panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/supprimer/<int:item_id>/', views.supprimer_item, name='supprimer_item'),
]
