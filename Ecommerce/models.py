from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
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



class User(AbstractUser):
    
    username = None


    groups = models.ManyToManyField(Group, related_name="ecommerce_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="ecommerce_user_permissions", blank=True)

    class Meta:
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
    


class Categorie(models.Model):
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    nom = models.CharField(max_length=255)
    description = models.TextField()

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
    


class SousCategorie(models.Model):

    class Meta:
        verbose_name = "Sous Catégorie"
        verbose_name_plural = "Sous Catégories"
    
    nom = models.CharField(max_length=255)
    description = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="categorie_souscategorie")

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
    


class Produit(models.Model):

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
   
    nom = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField()
    image = models.ImageField(upload_to='produits/')
    souscategorie = models.ForeignKey(SousCategorie, on_delete=models.CASCADE, related_name="souscategorie_produit")

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
    


class Panier(models.Model):

    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"
   
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name='panier_user')
    reduction = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    prixTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"panier {self.id} de {self.utilisateur.nom} {self.utilisateur.prenom}"

    
    
class PanierItem(models.Model):

    class Meta:
        verbose_name = "Panier Item"
        verbose_name_plural = "Paniers Items"
    
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.total
    


class Commande(models.Model):

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
    
    prixtotal = models.DecimalField(max_digits=10, decimal_places=2)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    inorder = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    deliver = models.BooleanField(default=False)
    fichierFacture = models.FileField(upload_to='factures/', null=True, blank=True)

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Commande {self.id} de {self.utilisateur.nom} {self.utilisateur.prenom}"
    


class Facture(models.Model):

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"

    
    commande = models.OneToOneField('Commande', on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    paiement_effectue = models.BooleanField(default=False)
    statut = models.CharField(max_length=20, choices=[('payée', 'Payée'), ('non_payée', 'Non payée')], default='non_payée')
    taxes = models.DecimalField(max_digits=5, decimal_places=2)
    

    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Facture N°{self.id} de la {self.commande.id} du client {self.utilisateur.nom} {self.utilisateur.prenom}"
    


class Coupon(models.Model):

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"
    
    code = models.CharField(max_length=50, unique=True)
    valeur = models.DecimalField(max_digits=5, decimal_places=2)  # Pourcentage de réduction
    expiration = models.DateTimeField()
    commande = models.OneToOneField('Commande', on_delete=models.CASCADE, related_name="commande_coupon", null=True, blank=True)
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Coupon {self.id} sur la commande N°{self.commande.id}"
    


class Expedition(models.Model):

    class Meta:
        verbose_name = "Expédition"
        verbose_name_plural = "Expéditions"
    
    adresse = models.TextField()
    dateExpedition = models.DateTimeField()
    dateLivraison = models.DateTimeField()
    commande = models.OneToOneField('Commande', on_delete=models.CASCADE) 
    

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.adresse
    


class Favoris(models.Model):

    class Meta:
        verbose_name = "Favoris"
        verbose_name_plural = "Favoris"
   
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)



class Blog(models.Model):

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blog"
    
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    cartepublication = models.DateTimeField(auto_now_add=True)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="categorie_blog")
    contenu = CKEditor5Field('Text', config_name='extends')

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre
    


class Commentaire(models.Model):

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
    
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    contenu = models.TextField()

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre
    


class Tags(models.Model):

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
    
    titre = models.CharField(max_length=255)

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre
    


class Paiement(models.Model):

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"

    class Methode(models.TextChoices):
        WAVES = "waves", "Waves"
        ORANGE = "orange", "Orange"
        ESPECE = "espece", "Espèce"
    
    methode = models.CharField(max_length=100, choices=Methode.choices, default=Methode.ESPECE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.methode
    


class Avis(models.Model):

    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    note = models.PositiveIntegerField()
    commentaire = models.TextField()
    

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.note
    


class Livreur(models.Model):

    class Meta:
        verbose_name = "Livreur"
        verbose_name_plural = "Livreurs"

    class Gender(models.TextChoices):
        MALE = "H", "Homme"
        FEMALE = "F", "Femme"
       
    class Language(models.TextChoices):
        ANG = "AN", "Anglais"
        FR = "FR", "Français"
        ALL = "AL", "Allemand"


    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    genre = models.CharField(max_length=1, choices=Gender.choices)
    experience = models.TextField()
    langue = models.CharField(max_length=2, choices=Language.choices, default=Language.FR)
    competence = models.CharField(max_length=20)
    datenaiss = models.CharField(max_length=20)
    numero = models.CharField(max_length=20)
    adresse = models.TextField()
    photo = models.ImageField(upload_to='livreurs/')
    email = models.EmailField(unique=True)

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class Faq(models.Model):
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    
    question = models.TextField()
    reponse = models.TextField()
    

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Politique(models.Model):

    class Meta:
        verbose_name = "Politique de confidentialité"
        verbose_name_plural = "Politiques de confidentialité"

    titre = models.CharField(max_length=255, default="Politique de confidentialité")
    contenu = CKEditor5Field('Contenu')
    
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return self.titre
    


class Conditions(models.Model):

    class Meta:
        verbose_name = "Condition d'utilisation"
        verbose_name_plural = "Conditions d'utilisation"

    titre = models.CharField(max_length=255, default="Conditions Générales d'Utilisation")
    contenu = CKEditor5Field('Contenu')
   
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.titre
    



class Propos(models.Model):

    class Meta:
        verbose_name = "A propos de nous"
        verbose_name_plural = "A propos de nous"

    titre = models.CharField(max_length=255)
    soustitre = models.CharField(max_length=255)
    description = CKEditor5Field('description')
    contenu = CKEditor5Field('Contenu')
    image = models.ImageField(upload_to='about/principale/')
    photo = models.ImageField(upload_to='about/secondaire/')
    nom = models.CharField(max_length=255)
    histore = CKEditor5Field('histoire')
    portrait = models.ImageField(upload_to="about/propos/")
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre




class Equipe(models.Model):

    class Meta:
        verbose_name = "Notre équipe"
        verbose_name_plural = "Notre équipe"

    nom = models.CharField(max_length=100)
    poste = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    photo = models.ImageField(upload_to='about/equipe/')

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} - {self.poste}"