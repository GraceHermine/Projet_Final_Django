from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import Blog, Commentaire,Categorie
from Ecommerce.models import Tags
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required


from django.utils.text import slugify
from django.core.paginator import Paginator


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

    paginator = Paginator(blogs, 6)  # 10 blogs par page
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

def blog_detail(request, slug):
    
    blog = get_object_or_404(Blog, slug=slug, statut=True)

    tags = Tags.objects.filter(statut=True)
    categories = Categorie.objects.all()
    related_posts = Blog.objects.filter(statut=True).order_by('-created_at')[:3]

    if request.method == "POST":
        if request.user.is_authenticated:
            contenu = request.POST.get("comment")
            parent_id = request.POST.get("parent_id")
            parent = Commentaire.objects.filter(id=parent_id).first() if parent_id else None

            if contenu and contenu:
                Commentaire.objects.create(
                    blog=blog,
                    utilisateur=request.user,
                    contenu=contenu,
                    parent=parent,
                    statut=True
                )
                messages.success(request, "Votre commentaire a été ajouté.")
                return redirect('blog_detail_page', slug=blog.slug)
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


# DEBUT DE LA GESTION DES ARTICLES DEPUIS L'INTERFACE DU SITE
# Soumission d’un article

@login_required
def soumettre_article(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        contenu = request.POST.get('contenu')
        categorie_id = request.POST.get('categorie_id')

        article = Blog.objects.create(
            titre=titre,
            slug=slugify(titre),  # <-- AJOUT DU SLUG
            image=image,
            description=description,
            contenu=contenu,
            auteur=request.user,
            categorie_id=categorie_id,
            statut=False  # En attente de validation
        )

        return redirect('mes_articles')
    
    categories = Categorie.objects.filter(statut=True)
    tags = Tags.objects.filter(statut=True)
    return render(request, 'soumettre_article.html', {'categories': categories, 'tags': tags})




# Articles de l'utilisateur connecté
@login_required
def mes_articles(request):
    articles = Blog.objects.filter(auteur_id=request.user).order_by('-created_at')
    categories = Categorie.objects.all()
    tags = Tags.objects.all()
    return render(request, "mes_articles.html", {"articles": articles,"categories": categories, "tags": tags})

# Page admin - articles en attente
@staff_member_required
def articles_en_attente(request):
    articles = Blog.objects.filter(statut=False).order_by('-created_at')
    return render(request, 'articles_en_attente.html', {'articles': articles})

# Action admin - valider un article
@staff_member_required
def valider_article(request, slug):
    article = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        article.statut = True
        article.save()
        return redirect('articles_en_attente')
    return redirect('articles_en_attente')


@login_required
def ajouter_article(request):
    categories = Categorie.objects.all()
    tags = Tags.objects.all()

    if request.method == "POST":
        titre = request.POST.get("titre")
        image = request.FILES.get("image")
        resume = request.POST.get("resume")
        contenu = request.POST.get("contenu")
        categorie_id = request.POST.get("categorie")
        tags_ids = request.POST.getlist("tags")
        statut = request.POST.get("statut") == "on"
        date_publication = request.POST.get("date_publication")
        
        categorie = Categorie.objects.get(id=categorie_id) if categorie_id else None
        tags_selected = Tags.objects.filter(id__in=tags_ids)

        article = Blog.objects.create(
            titre=titre,
            image=image,
            resume=resume,
            contenu=contenu,
            slug=slugify(titre),
            statut=statut,
            auteur_id=request.user,
            categorie_id=categorie,
            date_de_publication=date_publication,
        )
        article.tag_ids.set(tags_selected)

        return redirect("index")

    return render(request, "soumettre_article.html", {"categories": categories, "tags": tags})

def modifier_article(request, article_id):
    article = get_object_or_404(Blog, id=article_id, auteur_id=request.user)

    if request.method == "POST":
        article.titre = request.POST.get("titre")
        article.description = request.POST.get("description")
        article.contenu = request.POST.get("contenu")

        # Gestion de l'image (si un nouveau fichier est fourni)
        if "image" in request.FILES:
            article.image = request.FILES["image"]

        # Mise à jour de la catégorie
        categorie_id = request.POST.get("categorie")
        article.categorie_id = Categorie.objects.get(id=categorie_id) if categorie_id else None

        # Mise à jour des tags
        tags_ids = request.POST.getlist("tags")
        article.tag_ids.set(Tags.objects.filter(id__in=tags_ids))

        # Mise à jour du statut de publication
        article.statut = request.POST.get("statut") == "on"

        # Sauvegarde des articles
        article.save()
        return redirect("mes_articles")

    return redirect("mes_articles")

@login_required
def supprimer_article(request, article_id):
    article = get_object_or_404(Blog, id=article_id, auteur_id=request.user)
    article.delete()
    return redirect("mes_articles")
