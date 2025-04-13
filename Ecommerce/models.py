from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _
from authentification.models import User


class Categorie(models.Model):
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    nom = models.CharField(max_length=255)
    description = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sous_categories')

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
   
    pour_slider = models.BooleanField(default=False, verbose_name="Afficher dans le slider")
    en_promotion = models.BooleanField(default=False, verbose_name="Produit en promotion")
    prix_promo = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Prix promotionnel"
    )

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom

    def get_prix_affiche(self):
        """Retourne le prix remisé s'il existe, sinon le prix normal"""
        if self.en_promotion and self.prix_promo:
            return self.prix_promo
        return self.prix
    
    @property
    def reduction_percent(self):
        if self.en_promotion and self.prix_promo:
            return round(100 - (self.prix_promo / self.prix * 100))
        return 0
    
    @property
    def prix_final(self):
        if self.en_promotion and self.prix_promo:
            return self.prix_promo
        return self.prix


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

    @property
    def total(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Commande {self.id} de {self.utilisateur.nom} {self.utilisateur.prenom}"
    

class CommandeItem(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name="items")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom} (Commande {self.commande.id})"

    @property
    def total_price(self):
        return self.quantite * self.prix_unitaire
 

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

