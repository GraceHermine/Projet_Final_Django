# Ecommerce/context_processors.py

from .models import Favoris, Panier, PanierItem

def favoris_count(request):
    if request.user.is_authenticated:
        count = Favoris.objects.filter(utilisateur=request.user).count()
    else:
        count = 0
    return {
        'favoris_count': count
    }

def panier_context(request):
    if request.user.is_authenticated:
        try:
            panier = Panier.objects.get(utilisateur=request.user)
            items = PanierItem.objects.filter(panier=panier)
            total = sum(item.total for item in items)
            quantite = sum(item.quantite for item in items)
        except Panier.DoesNotExist:
            items = []
            total = 0
            quantite = 0
    else:
        items = []
        total = 0
        quantite = 0

    return {
        'mini_panier_items': items,
        'mini_panier_total': total,
        'mini_panier_quantite': quantite,
    }
