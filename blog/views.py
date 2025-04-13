from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from Ecommerce.models import Blog, Commentaire,Temoignage,Avis,Facture, Favoris, Panier, PanierItem, User, Produit, Faq, Politique, Conditions, Propos, Equipe,Categorie,Tags,SousCategorie,Commande,CommandeItem
from django.db.models import Q



# Create your views here.
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
    blog = Blog.objects.get(id=blog_id)

    tags = Tags.objects.filter(statut=True)
    categories = Categorie.objects.all()
    related_posts = Blog.objects.exclude(id=blog_id).filter(statut=True)[:3]

    if request.method == "POST":
        if request.user.is_authenticated:
            titre = request.POST.get("titre")
            contenu = request.POST.get("comment")
            parent_id = request.POST.get("parent_id")
            parent = Commentaire.objects.filter(id=parent_id).first() if parent_id else None

            if titre and contenu:
                Commentaire.objects.create(
                    blog=blog,
                    utilisateur=request.user,
                    titre=titre,
                    contenu=contenu,
                    parent=parent,
                    statut=True
                )
                messages.success(request, "Votre commentaire a été ajouté.")
                return redirect('blog-detail', blog_id=blog.id)
            else:
                messages.error(request, "Tous les champs sont obligatoires.")

    commentaires = blog.commentaire_set.filter(parent__isnull=True, statut=True).order_by('-created_at')
    blog_commentaire_count = blog.commentaire_set.filter(statut=True).count()

    datas = {
        "blog": blog,
        "commentaires": commentaires,
        "blog_commentaire_count": blog_commentaire_count,
        "categories": categories,
        "related_posts": related_posts,
        "tags": tags,
    }

    return render(request, 'blog-details.html', datas)