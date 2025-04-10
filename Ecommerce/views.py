from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Blog, Commentaire, Favoris, Panier, PanierItem, User, Produit, Faq, Politique, Conditions, Propos, Equipe,Categorie,Tags

# Create your views here.

# Debut de l'authentification
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')  # ou autre page après connexion
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Un compte avec cet email existe déjà.")
        else:
            user = User.objects.create_user(
                email=email,
                password=password,
                nom=nom,
                prenom=prenom
            )
            messages.success(request, "Compte créé avec succès. Connectez-vous maintenant.")
            return redirect('login')

    return render(request, 'login.html')

def logout(request):
    django_logout(request)
    return redirect('login')
# Fin de l'authentification


# Debut du code de la page index qu est la page d'accueille 
def index(request):
    blogs_home = Blog.objects.filter(statut=True)[:6]
    produits_recent = Produit.objects.filter(statut=True).order_by("-created_at")[:4]
    favoris_ids = []

    if request.user.is_authenticated:
        favoris_ids = list(Favoris.objects.filter(utilisateur=request.user).values_list('produit_id', flat=True))
    datas = {
        "blogs":blogs_home,
        "produits":produits_recent,
        'favoris_ids': favoris_ids,
    }
    return render(request, 'index.html', datas)
# Fin de la partie index


# Début du about
def about(request):

    membres = Equipe.objects.filter(statut=True)
    
    propos = Propos.objects.filter(statut=True).first()
    datas = {
        
        'propos': propos,
        'membres': membres,
    }

    return render(request, 'about.html', datas)
#  Fin du about

# Debut du code du blog ainsi que le blog détail
def blog(request):
    query = request.GET.get('q')  # Récupère le texte de recherche
    categories = Categorie.objects.all()
    tags = Tags.objects.filter(statut=True)
    blogs = Blog.objects.filter(statut=True)
    
    if query:
        blogs = blogs.filter(
            Q(titre__icontains=query)
        )

    paginator = Paginator(blogs, 10)  # 10 blogs par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    recent_blogs = Blog.objects.filter(statut=True).order_by('-created_at')[:5]
    commentaires = Commentaire.objects.filter(statut=True).order_by('-created_at')[:5]
    
    
    datas = {
        "page_obj": page_obj,
        "commentaires": commentaires,
        "recent_blogs": recent_blogs,
        "query": query,  # Pour réafficher dans le champ input si nécessaire
        "categories": categories,
        "tags": tags, 
        
    }
    
    return render(request, 'blog.html', datas)

def blog_detail(request, blog_id):
    # Récupérer l'article actuel
    blog = Blog.objects.get(id=blog_id)
    tags = Tags.objects.filter(statut=True)
    # Récupérer toutes les catégories (si tu veux afficher des catégories liées aussi)
    categories = Categorie.objects.all()
    
    # Récupérer les articles liés en excluant l'article actuel
    related_posts = Blog.objects.exclude(id=blog_id).filter(statut=True)[:4]  # Limiter à 4 articles
    
    if request.method == "POST":
        if request.user.is_authenticated:
            titre = request.POST.get("titre")
            contenu = request.POST.get("comment")

            if titre and contenu:
                Commentaire.objects.create(
                    blog=blog,
                    utilisateur=request.user,
                    titre=titre,
                    contenu=contenu,
                    statut=True  # ou False si tu veux une validation manuelle
                )
                messages.success(request, "Votre commentaire a été ajouté.")
                return redirect('blog-detail', blog_id=blog.id)
            else:
                messages.error(request, "Tous les champs sont obligatoires.")
    
    # Récupérer les commentaires
    commentaires = blog.commentaire_set.filter(statut=True).order_by('-created_at')
    blog_commentaire_count = commentaires.count()

    # Passer les données au template
    datas = {
        "blog": blog,
        "commentaires": commentaires,
        "blog_commentaire_count": blog_commentaire_count,
        "categories": categories,
        "related_posts": related_posts,  # Passer les articles liés
        "tags": tags, 
    }

    return render(request, 'blog-details.html', datas)


# Fin du blog & blog détail

# Debut du code de la partie shop
@login_required
def ajouter_au_panier(request, produit_id):
    if request.method == "POST":
        produit = get_object_or_404(Produit, id=produit_id)
        quantite = int(request.POST.get('quantite', 1))

        panier, created = Panier.objects.get_or_create(utilisateur=request.user)

        item, item_created = PanierItem.objects.get_or_create(
            panier=panier,
            produit=produit,
            defaults={
                'quantite': quantite,
                'total': quantite * produit.prix
            }
        )

        if not item_created:
            item.quantite += quantite
            item.total = item.quantite * produit.prix
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

    datas = {
        "produit": produit,
        "produits": produits,
        "favoris": favoris
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

def shop(request):
    produits = Produit.objects.filter(statut=True)
    produits_recent = Produit.objects.filter(statut=True).order_by("-created_at")
    favoris_ids = []

    paginator = Paginator(produits, 12)  # 12 produits par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        favoris_ids = list(Favoris.objects.filter(utilisateur=request.user).values_list('produit_id', flat=True))
    datas = {
        "page_obj": page_obj,
        "produits":produits,
        'favoris_ids': favoris_ids,
        "produits_recent": produits_recent

    }
    return render(request, 'shop-right-sidebar.html', datas)
# Fin de la partie shop


def contact(request):
    datas = {
    

    }
    return render(request, 'contact.html', datas)

def service(request):
    conditions = Conditions.objects.filter(statut=True).order_by('created_at')
    datas = {
        'cond': conditions
    }
    return render(request, 'services.html', datas)

def account(request):
    datas = {

    }
    return render(request, 'my-account.html', datas)

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.prenom = request.POST.get('first_name', user.prenom)
        user.nom = request.POST.get('last_name', user.nom)
        user.email = request.POST.get('email', user.email)
        user.genre = request.POST.get('gender', user.genre)

        datenaiss = request.POST.get('birthday')
        if datenaiss:
            user.datenaiss = datenaiss

        # user.optin = bool(request.POST.get('optin'))
        # user.newsletter = bool(request.POST.get('newsletter'))

        user.save()
        messages.success(request, "Profil mis à jour avec succès.")
        return redirect('account')

def wishlist(request):
    favoris_user = Favoris.objects.filter(utilisateur=request.user)
    datas = {
        "list_favoris":favoris_user,
    }
    return render(request, 'wishlist.html', datas)

def policy(request):
    politique = Politique.objects.filter(statut=True).order_by('created_at')
    
    datas = {
        'politique': politique
    }
    return render(request, 'privacy-policy.html', datas)

def notfound(request):
    datas = {

    }
    return render(request, '404.html', datas)

def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirige si l'utilisateur n'est pas connecté

    try:
        panier = Panier.objects.get(utilisateur=request.user)
    except Panier.DoesNotExist:
        panier = Panier.objects.create(utilisateur=request.user)

    panier_items = PanierItem.objects.filter(panier=panier)

    # Calcul du total
    total = sum(item.produit.prix * item.quantite for item in panier_items)

    for item in panier_items:
        item.total = item.produit.prix * item.quantite  # attribut temporaire
    datas = {
        'panier_items': panier_items,
        'total': total
    }
    return render(request, 'cart.html', datas)

def checkout(request):
    datas = {

    }
    return render(request, 'checkout.html', datas)


def faq(request):
    faqs = Faq.objects.filter(statut=True).order_by('-created_at')

    datas = {
        'faqs': faqs
    }
    return render(request, 'faq.html', datas)



