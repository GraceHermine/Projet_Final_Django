import uuid
# from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.utils import timezone

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager



class UserManager(BaseUserManager):

    class Meta:
        app_label = 'Ecommerce'
        
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crée et retourne un superutilisateur avec un email.
        """
        if not email:
            raise ValueError("L'email doit être défini")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Crée un utilisateur normal avec un email.
        """
        if not email:
            raise ValueError("L'email doit être défini")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

# Il doit bouger hein


class User(AbstractUser):
    
    username = None


    groups = models.ManyToManyField(Group, related_name="ecommerce_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="ecommerce_user_permissions", blank=True)

    class Meta:
        app_label = 'Ecommerce'
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    class Gender(models.TextChoices):
        MALE = "H", _("Homme")
        FEMALE = "F", _("Femme")

    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    genre = models.CharField(max_length=1, choices=Gender.choices, null=True)
    datenaiss = models.DateField(null=True)
    numero = models.CharField(max_length=15, null=True, validators=[
            RegexValidator(
                regex=r"^225 \d{10}$",
                message="Le numéro doit commencer par 225 et contenir exactement 8 chiffres après l'indicatif.",
                code="invalid_phone_number"
            )
        ],
        unique=True)
    adresse = models.TextField(null=True)
    photo = models.ImageField(upload_to='users/', blank=True, null=True)
    email = models.EmailField(unique=True)
    panier = models.OneToOneField('Panier', on_delete=models.SET_NULL, null=True, blank=True, related_name="utilisateur_panier")
    

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    





class PasswordResetCode(models.Model):
    email = models.EmailField(null=True, blank=True) # Ce champ doit être présent pour recevoir l'email de l'utilisateur
    code = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def is_valid(self):
        # Le code est valide s'il a moins de 5 minutes
        return (timezone.now() - self.created_at).total_seconds() < 300
    



