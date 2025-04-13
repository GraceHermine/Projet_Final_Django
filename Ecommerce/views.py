from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Prefetch, Avg, Count
from .utils import generate_invoice_pdf
from django.http import HttpResponse, HttpResponseForbidden
from .models import Avis,Facture, Favoris, Panier, PanierItem, Produit, Categorie,SousCategorie,Commande,CommandeItem,Coupon,Expedition
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO
from blog.models import Blog
from siteinfo.models import Temoignage
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
# Create your views here.



# Debut de l'authentification



# Debut du code de la page index qu est la page d'accueille 
def index(request):
    
    blogs_home = Blog.objects.filter(statut=True)[:6]
    produits_recent = Produit.objects.filter(statut=True).order_by("-created_at")[:6]
    produits_slider = Produit.objects.filter(pour_slider=True, statut=True)
    produits_promo = Produit.objects.filter(statut=True, en_promotion=True).order_by('-created_at')[:3]

    # Favoris de l'utilisateur connecté
    favoris_ids = []
    if request.user.is_authenticated:
        favoris_ids = list(
            Favoris.objects.filter(utilisateur=request.user).values_list('produit_id', flat=True)
        )

    # Produits à afficher dans une section "Top catégories cette semaine"
    categories_top = SousCategorie.objects.filter(statut=True)[:5]
    produit_par_categorie_top = []

    for sous_cat in categories_top:
        produit = Produit.objects.filter(souscategorie=sous_cat, statut=True).first()
        if produit:
            produit_par_categorie_top.append({
                'categorie': sous_cat,
                'produit': produit
            })

    # Produits groupés par catégorie (section "Featured", "Laptop", etc.)
    categories_a_afficher = Categorie.objects.filter(statut=True).order_by('nom')[:4]
    produits_par_categorie = []
    for categorie in categories_a_afficher:
        produits = Produit.objects.filter(souscategorie__categorie=categorie, statut=True).order_by('-created_at')[:6]
        produits_par_categorie.append({
            'categorie': categorie,
            'produits': produits
        })

    cat_femme = Produit.objects.filter(souscategorie__nom="Menche longue", statut=True)[:10]
    cat_menche = Produit.objects.filter(souscategorie__nom__iexact="Menche courte", statut=True)[:10]
    temoignages = Temoignage.objects.filter(statut=True).order_by('-created_at')[:5]
    
    # Contexte final envoyé au template
    datas = {

        "blogs": blogs_home,
        "produits": produits_recent,
        "produits_slider": produits_slider,
        "produits_promo": produits_promo,
        "favoris_ids": favoris_ids,
        "produit_par_categorie_top": produit_par_categorie_top,
        "produits_par_categorie": produits_par_categorie,
        'cat_femme': cat_femme,
        'menche': cat_menche,
        'temoignages': temoignages,
        
        
    }

    return render(request, 'index.html', datas)







# Debut du code de la partie shop
@login_required
def ajouter_au_panier(request, produit_id):
    if request.method == "POST":
        produit = get_object_or_404(Produit, id=produit_id)
        quantite = int(request.POST.get('quantite', 1))
        prix_utilise = produit.prix_final
        panier, created = Panier.objects.get_or_create(utilisateur=request.user)

        item, item_created = PanierItem.objects.get_or_create(
            panier=panier,
            produit=produit,
            defaults={
                'quantite': quantite,
                'total': quantite * prix_utilise 
            }
        )

        if not item_created:
            item.quantite += quantite
            item.total = item.quantite * prix_utilise 
            item.save()

        # mettre à jour le prix total du panier
        items = PanierItem.objects.filter(panier=panier)
        panier.prixTotal = sum(i.total for i in items)
        panier.save()

        return redirect('produit', produit_id=produit.id)
    
@login_required
def supprimer_item(request, item_id):
    item = PanierItem.objects.get(id=item_id)
    if item.panier.utilisateur == request.user:
        item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'cart'))

def produit(request, produit_id):
    produit = Produit.objects.get(id=produit_id)
    produits = Produit.objects.filter(statut=True)[:4]

    favoris = None
    if request.user.is_authenticated:
        favoris = Favoris.objects.filter(utilisateur=request.user, produit=produit).first()

    avis_stats = Avis.objects.filter(Produit=produit, statut=True).aggregate(
        moyenne=Avg('note'),
        total=Count('id')
    )
    avis_list = Avis.objects.filter(Produit=produit, statut=True).order_by('-created_at')
    categories = Categorie.objects.filter()
    cat_femme = Produit.objects.filter(souscategorie__nom="Menche longue", statut=True)[:10]
    cat_menche = Produit.objects.filter(souscategorie__nom__iexact="Menche courte", statut=True)[:10]

    datas = {
        "produit": produit,
        "produits": produits,
        "favoris": favoris,
        "note_moyenne": avis_stats['moyenne'] or 0,
        "total_avis": avis_stats['total'],
        "avis_list": avis_list,
        "categories": categories,
        'cat_femme': cat_femme,
        'menche': cat_menche,

    }
    return render(request, 'product-sidebar.html', datas)

@login_required
def ajouter_favoris(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    Favoris.objects.get_or_create(utilisateur=request.user, produit=produit)
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def supprimer_favoris(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    favoris = Favoris.objects.filter(utilisateur=request.user, produit=produit)
    favoris.delete()
    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
def ajouter_avis(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    if request.method == "POST":
        note = int(request.POST.get("note"))
        commentaire = request.POST.get("commentaire")

        # Empêcher de publier plusieurs avis (optionnel)
        ancien_avis = Avis.objects.filter(user=request.user, Produit=produit).first()
        if ancien_avis:
            messages.warning(request, "Vous avez déjà laissé un avis pour ce produit.")
        else:
            Avis.objects.create(
                user=request.user,
                Produit=produit,
                note=note,
                commentaire=commentaire,
                statut=True
            )
            messages.success(request, "Votre avis a été ajouté avec succès.")

    return redirect("produit", produit_id=produit_id)


def get_context_produits(request, produits):
    paginator = Paginator(produits, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Categorie.objects.filter(statut=True).prefetch_related(
        Prefetch(
            "categorie_souscategorie",
            queryset=SousCategorie.objects.filter(statut=True)
        )
    )

    return {
        "page_obj": page_obj,
        "categories": categories,
    }

def shop_by_categorie(request, cat_id):
    categorie = get_object_or_404(Categorie, id=cat_id)
    souscategories = SousCategorie.objects.filter(categorie=categorie, statut=True)
    produits = Produit.objects.filter(souscategorie__in=souscategories, statut=True)

    context = get_context_produits(request, produits)
    context["selected_categorie"] = categorie
    return render(request, "shop-right-sidebar.html", context)

def shop_by_souscategorie(request, scat_id):
    souscategorie = get_object_or_404(SousCategorie, id=scat_id)
    produits = Produit.objects.filter(souscategorie=souscategorie, statut=True)

    context = get_context_produits(request, produits)
    context["selected_souscategorie"] = souscategorie
    return render(request, "shop-right-sidebar.html", context)


def shop(request):
    order_by = request.GET.get("orderby", "-created_at")  # Valeur par défaut = les plus récents

    produits = Produit.objects.filter(statut=True)

    # Gestion du tri par note
    if order_by == "-note_moyenne":
        produits = produits.annotate(note_moyenne=Avg("avis_produit__note")).order_by(order_by)
    else:
        produits = produits.order_by(order_by)

    # Produits récents inchangés (toujours les plus récents)
    produits_recent = Produit.objects.filter(statut=True).order_by("-created_at")[:4]

    # Gestion des favoris de l'utilisateur
    favoris_ids = []
    if request.user.is_authenticated:
        favoris_ids = list(
            Favoris.objects.filter(utilisateur=request.user).values_list('produit_id', flat=True)
        )

     # Catégories avec sous-catégories
    categories = Categorie.objects.filter(statut=True).prefetch_related(
        "categorie_souscategorie"
    )

    # Pagination : 12 produits par page
    paginator = Paginator(produits, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    datas = {
        "page_obj": page_obj,
        "produits": produits,  # optionnel ici, utilisé ?
        "favoris_ids": favoris_ids,
        "produits_recent": produits_recent,
        "total_resultats": paginator.count,
        "page_debut": (page_obj.start_index() if paginator.count > 0 else 0),
        "page_fin": (page_obj.end_index() if paginator.count > 0 else 0),
        "orderby": order_by,  # pour pré-sélectionner l'option dans le <select>
        "categories": categories,
    }

    return render(request, 'shop-right-sidebar.html', datas)
# Fin de la partie shop




def wishlist(request):
    favoris_user = Favoris.objects.filter(utilisateur=request.user)
    datas = {
        "list_favoris":favoris_user,
    }
    return render(request, 'wishlist.html', datas)



def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirige si l'utilisateur n'est pas connecté

    try:
        panier = Panier.objects.get(utilisateur=request.user)
    except Panier.DoesNotExist:
        panier = Panier.objects.create(utilisateur=request.user)

    panier_items = PanierItem.objects.filter(panier=panier)

    # ✅ Calcul du total avec prix promo si actif
    total = sum(item.produit.prix_final * item.quantite for item in panier_items)

    # ✅ Attribut temporaire pour chaque item (si pas déjà dans le modèle)
    for item in panier_items:
        item.total = item.produit.prix_final * item.quantite

    datas = {
        'panier_items': panier_items,
        'total': total
    }
    return render(request, 'cart.html', datas)





def proceed_to_checkout(request):
    if not request.user.is_authenticated:
        messages.error(request, "Veuillez vous connecter pour finaliser la commande.")
        return redirect("login")

    panier = Panier.objects.filter(utilisateur=request.user).first()
    panier_items = PanierItem.objects.filter(panier=panier).all()

    if panier is None:
        messages.error(request, "Votre panier est vide.")
        return redirect("cart")

    total = sum(item.quantite * item.produit.prix_final for item in panier_items)
    
    commande = Commande.objects.create(
        utilisateur=request.user,
        prixtotal=total,
        statut=True,
    )

    for item in panier_items:
        CommandeItem.objects.create(
            commande=commande,
            produit=item.produit,
            quantite=item.quantite,
            prix_unitaire=item.produit.prix_final,
        )
        item.delete()

    panier.delete()

    return redirect("checkout", commande_id=commande.id)



def checkout(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    items = commande.items.all()
    cart_subtotal = commande.prixtotal
    shipping_cost = 1500
    total_commande = commande.prixtotal + shipping_cost

    if request.method == 'POST':
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        ville = request.POST.get('ville')
        adresse_complement = request.POST.get('adresse_complement')
        quartier = request.POST.get('quartier')
        numero = request.POST.get('numero')
        email = request.POST.get('email')

        coupon_code = request.POST.get('coupon_code')
        reduction = 0

        if coupon_code:
            coupon = Coupon.objects.filter(code=coupon_code, expiration__gte=timezone.now(), statut=True).first()
            if coupon:
                reduction = coupon.valeur
                commande.prixtotal = commande.prixtotal * (1 - (reduction / 100))
                coupon.commande = commande
                coupon.save()
            else:
                messages.warning(request, "Code promo invalide ou expiré.")

        total_commande = commande.prixtotal + shipping_cost

        facture, created = Facture.objects.get_or_create(
            commande=commande,
            defaults={
                'utilisateur': request.user,
                'montant': total_commande,
                'statut': 'non_payée',
                'taxes': 0,
            }
        )

        facture.save()

        return redirect('payment', facture_id=facture.id)

    return render(request, 'checkout.html', {
        'commande': commande,
        'items': items,
        'cart_subtotal': cart_subtotal,
        'shipping_cost': shipping_cost,
        'order_total': total_commande,
    })

@login_required
def payment(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    pdf_buffer = generate_invoice_pdf(facture.commande, facture)
    envoyer_facture_par_email(facture, facture.commande, pdf_buffer)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if payment_method not in ['orange_money', 'wave', 'cash_on_delivery']:
            messages.error(request, "Méthode de paiement invalide. Veuillez réessayer.")
            return redirect('payment', facture_id=facture.id)

        if payment_method == 'orange_money':
            facture.statut = 'payée'
            facture.save()
            messages.success(request, "Votre paiement via Orange Money a été confirmé.")
            return redirect('order_confirmation', commande_id=facture.commande.id)

        elif payment_method == 'wave':
            facture.statut = 'payée'
            facture.save()
            messages.success(request, "Votre paiement via Wave a été confirmé.")
            return redirect('order_confirmation', commande_id=facture.commande.id)

        elif payment_method == 'cash_on_delivery':
            facture.statut = 'en attente de paiement'
            facture.save()
            messages.success(request, "Vous avez choisi de payer en espèces lors de la livraison.")
            return redirect('order_confirmation', commande_id=facture.commande.id)

    return render(request, 'payment.html', {'facture': facture})

def generate_invoice_pdf(commande, facture):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Facture de Commande")

    p.setFont("Helvetica", 12)
    p.drawString(100, height - 80, f"Numéro de commande : {commande.id}")
    # p.drawString(100, height - 100, f"Date : {facture.date.strftime('%d/%m/%Y')}")  # Uses new date field
    p.drawString(100, height - 120, f"Client : {facture.utilisateur.prenom} {facture.utilisateur.nom}")
    p.drawString(100, height - 140, f"Email : {facture.utilisateur.email}")
    # p.drawString(100, height - 160, f"Adresse : {facture.utilisateur.adresse}, {facture.utilisateur.ville}")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, height - 200, "Détails de la commande")
    p.setFont("Helvetica", 10)

    y = height - 220
    cart_subtotal = 0
    for item in commande.items.all():
        item_total = item.produit.prix * item.quantite
        cart_subtotal += item_total
        p.drawString(100, y, f"{item.produit.nom} x {item.quantite}")
        p.drawString(400, y, f"{item_total} FCFA")
        y -= 20

    shipping_cost = 1500
    order_total = cart_subtotal + shipping_cost

    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y - 20, "Sous-total :")
    p.drawString(400, y - 20, f"{cart_subtotal} FCFA")
    p.drawString(100, y - 40, "Frais de livraison :")
    p.drawString(400, y - 40, f"{shipping_cost} FCFA")
    p.drawString(100, y - 60, "Total :")
    p.drawString(400, y - 60, f"{order_total} FCFA")

    p.drawString(100, y - 80, f"Statut : {facture.get_statut_display()}")

    p.setFont("Helvetica-Oblique", 10)
    p.drawString(100, 50, "Merci pour votre achat !")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def order_confirmation(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    facture = get_object_or_404(Facture, commande=commande)

    if facture.utilisateur != request.user:
        return HttpResponseForbidden("Accès non autorisé")

    items = commande.items.all()
    for item in items:
        item.item_total = item.produit.prix * item.quantite

    cart_subtotal = sum(item.item_total for item in items)
    shipping_cost = 1500
    order_total = cart_subtotal + shipping_cost

    context = {
        'commande': commande,
        'facture': facture,
        'cart_subtotal': cart_subtotal,
        'shipping_cost': shipping_cost,
        'order_total': order_total,
    }

    return render(request, 'order_confirmation.html', context)

def download_invoice(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    facture = get_object_or_404(Facture, commande=commande)

    if facture.utilisateur != request.user:
        return HttpResponseForbidden("Accès non autorisé")

    pdf_buffer = generate_invoice_pdf(commande, facture)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{commande.id}.pdf"'
    response.write(pdf_buffer.getvalue())
    pdf_buffer.close()

    return response



def search(request):
    query = request.GET.get("q", "")
    produits = Produit.objects.filter(nom__icontains=query, statut=True)
    datas = get_context_produits(request, produits)
    datas["query"] = query
    return render(request, "shop-right-sidebar.html", datas)


def envoyer_facture_par_email(facture, commande, pdf_buffer):
    subject = f"Confirmation de votre commande #{commande.id}"
    message = render_to_string("facture.html", {
        "utilisateur": facture.utilisateur,
        "commande": commande,
        "facture": facture,
    })
    email = EmailMessage(subject, message, to=[facture.utilisateur.email])
    email.attach(f"facture_{commande.id}.pdf", pdf_buffer.getvalue(), "application/pdf")
    email.content_subtype = "html"
    email.send()



@login_required
def update_quantite(request, item_id):
    item = get_object_or_404(PanierItem, id=item_id, panier__utilisateur=request.user)
    if request.method == "POST":
        quantite = int(request.POST.get("quantite", 1))
        item.quantite = quantite
        item.total = quantite * item.produit.prix_final
        item.save()

        # Mise à jour du panier
        panier = item.panier
        panier.prixTotal = sum(i.total for i in PanierItem.objects.filter(panier=panier))
        panier.save()

    return redirect("cart")



@login_required
def suivi_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, utilisateur=request.user)
    expedition = Expedition.objects.filter(commande=commande).first()
    return render(request, 'suivi_commande.html', {
        'commande': commande,
        'expedition': expedition,
    })