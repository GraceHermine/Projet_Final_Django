from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.core.mail import send_mail
# from django.contrib.auth.models import User
from django.contrib import messages
from .models import PasswordResetCode
# from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.conf import settings
import random
import uuid
from Ecommerce.models import Commande
# from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

from django.contrib.auth.decorators import login_required
User = get_user_model()


# Create your views here.

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        username = request.POST.get('uname')

        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Cet email existe déjà.')
            return redirect('register')  # Redirection vers la page d'inscription
        
        user = User.objects.create_user(
            email=email,
            password=password,
            nom=firstname,
            prenom=lastname,
               # idem
        )
        
        # Envoi de mail de confirmation (facultatif, assure-toi que Django est bien configuré)
        subject = 'Confirmation d’inscription'
        message = 'Bonjour,\nVotre inscription sur notre site a été effectuée avec succès !'
        email_from = 'dedjeneg@gmail.com'
        send_mail(subject, message, email_from, [email], fail_silently=False)

        messages.success(request, 'Utilisateur enregistré avec succès !')
        return redirect('index')  # Redirection vers la page de connexion

    return render(request, 'register.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('uname').strip()
        password = request.POST.get('password').strip()

        user = authenticate(request, username=email, password=password)  # <- note 'username=email'

        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie !')
            return redirect('index')
        else:
            messages.error(request, 'Identifiants incorrects.')
            return redirect('login')

    return render(request, 'login.html')




def logout_view(request):
    logout(request)
    return redirect('index')

# 
def send_mail_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'insert_email.html', {"error": "Email non trouvé."})

        # Supprimer les anciens codes pour cet email
        PasswordResetCode.objects.filter(email=email).delete()

        # Générer un nouveau code et un token unique
        code = f"{random.randint(0, 999999):06}"
        token = str(uuid.uuid4())

        # Créer un nouvel enregistrement
        user = User.objects.get(email=email)
        reset_obj = PasswordResetCode.objects.create(email=email, code=code, token=token, user=user)
        # reset_obj = PasswordResetCode.objects.create(email=email, code=code, token=token)

        # Construire le lien de confirmation de putain d'igname kpognan
        confirm_url = request.build_absolute_uri(reverse('confirm_code', args=[token]))
        message = f"Votre code de réinitialisation est {code}. \nCliquez ici pour confirmer : {confirm_url}"

        # Envoyer l'email
        send_mail(
            'Réinitialisation de votre mot de passe',
            message,
            'hermine@notresite.com',
            [email],
            fail_silently=False,
        )

        return redirect('confirm_code', token=reset_obj.token)

    return render(request, 'insert_email.html')



def confirm_code_view(request, token):
    reset_obj = get_object_or_404(PasswordResetCode, token=token)
    error = None

    if request.method == 'POST':
        code_input = request.POST.get('code')
        if reset_obj.is_valid():
            if reset_obj.code == code_input:
                # Stocker l'email en session pour l'étape suivante
                request.session['reset_email'] = reset_obj.user.email

                # Générer l'URL de réinitialisation avec le token
                reset_url = reverse('reset_password', kwargs={'token': str(reset_obj.token)})

                # Rediriger vers la page de réinitialisation avec le token
                return redirect(reset_url)
            else:
                error = "Le code saisi est incorrect."
        else:
            error = "Le code a expiré."

    return render(request, 'verify_code.html', {'error': error, 'token': token})


def reset_password_view(request, token):
    try:
        token = uuid.UUID(token)  # Convertir le token en UUID pour éviter toute erreur
    except ValueError:
        return redirect('send_mail')  # Redirige si le token est invalide

    email = request.session.get('reset_email')
    if not email:
        return redirect('send_mail')

    error = None
    success = None

    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            error = "Les mots de passe ne correspondent pas."
        else:
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                user.password = make_password(password)
                user.save()
                success = "Votre mot de passe a été réinitialisé avec succès."

                # Supprimer les données de session
                del request.session['reset_email']

                return redirect('login')  # Redirige vers la connexion après succès

            except User.DoesNotExist:
                error = "Aucun utilisateur trouvé avec cet email."

    return render(request, 'reset_password.html', {'error': error, 'success': success, 'token': token})


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        user.prenom = request.POST.get('prenom')
        user.nom = request.POST.get('nom')
        user.email = request.POST.get('email')
        user.datenaiss = request.POST.get('datenaiss')
        user.numero = request.POST.get('numero')
        user.save()
        messages.success(request, "Vos informations ont été mises à jour.")
        return redirect('account')  # retour vers le dashboard

    return redirect('account')  # fallback




def account(request):
    commandes = Commande.objects.filter(utilisateur=request.user).order_by('-created_at')[:5]
    datas = {
        'commandes_recente': commandes
    }
    return render(request, 'my-account.html', datas)

