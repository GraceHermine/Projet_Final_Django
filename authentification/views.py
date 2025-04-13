from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from reportlab.lib.units import inch
from Ecommerce.models import  User


# Create your views here.
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
# Fin de l'authentification