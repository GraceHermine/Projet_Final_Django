from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title="API de mon eCommerce",
        default_version='v1',
        description="🚀 API REST complète pour la gestion du site e-commerce (produits, commandes, blogs, etc.)",
        terms_of_service="https://www.tonsite.com/cgu/",
        contact=openapi.Contact(email="contact@tonsite.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)


router = DefaultRouter()
# APPLICATION BLOG
router.register('blogs', BlogViewSet)
router.register('commentaires', CommentaireViewSet)

# APPLICATION SITEINFO
router.register('faq', FaqViewSet)
router.register('politiques', PolitiqueViewSet)
router.register('conditions', ConditionsViewSet)
router.register('propos', ProposViewSet)
router.register('equipe', EquipeViewSet)
router.register('temoignages', TemoignageViewSet)


# APPLICATION ECOMMERCE
router.register('categories', CategorieViewSet)
router.register('souscategories', SousCategorieViewSet)
router.register('produits', ProduitViewSet)

router.register('paniers', PanierViewSet)
router.register('panier-items', PanierItemViewSet)

router.register('commandes', CommandeViewSet)
router.register('commande-items', CommandeItemViewSet)
router.register('factures', FactureViewSet)

router.register('coupons', CouponViewSet)
router.register('expeditions', ExpeditionViewSet)
router.register('favoris', FavorisViewSet)
router.register('avis', AvisViewSet)
router.register('tags', TagsViewSet)
router.register('livreurs', LivreurViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

