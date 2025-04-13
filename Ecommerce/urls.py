from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
    path("shop/", views.shop, name="shop"),
    path("produit/<int:produit_id>/", views.produit, name="produit"),
    path('shop/categorie/<int:cat_id>/', views.shop_by_categorie, name='shop_by_categorie'),
    path('shop/souscategorie/<int:scat_id>/', views.shop_by_souscategorie, name='shop_by_souscategorie'),
    path("about/", views.about, name="about"),
    path("service/", views.service, name="service"),
    path("account/", views.account, name="account"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("policy/", views.policy, name="policy"),
    
    path("notfound/", views.notfound, name="notfound"),
    path('checkout/<int:commande_id>/', views.checkout, name='checkout'),
    path('payment/<int:facture_id>/', views.payment, name='payment'),
    path('order-confirmation/<int:commande_id>/', views.order_confirmation, name='order_confirmation'),
    path('download-invoice/<int:commande_id>/', views.download_invoice, name='download_invoice'),
    path('proceed-to-checkout/', views.proceed_to_checkout, name='proceed-to-checkout'),
    path("cart/", views.cart, name="cart"),
    path('faq/', views.faq, name='faq'),
    path('favoris/ajouter/<int:produit_id>/', views.ajouter_favoris, name='ajouter_favoris'),
    path('favoris/supprimer/<int:produit_id>/', views.supprimer_favoris, name='supprimer_favoris'),
    path('ajouter-au-panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/supprimer/<int:item_id>/', views.supprimer_item, name='supprimer_item'),
    path('produit/<int:produit_id>/avis/', views.ajouter_avis, name='ajouter_avis'),
]
