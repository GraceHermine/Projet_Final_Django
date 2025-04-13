from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _
# Create your models here.



class Faq(models.Model):
    class Meta:
        app_label = 'Ecommerce'
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
        app_label = 'Ecommerce'
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
        app_label = 'Ecommerce'
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
        app_label = 'Ecommerce'
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
        app_label = 'Ecommerce'
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
    


class Temoignage(models.Model):

    class Meta:
        app_label = 'Ecommerce'
        verbose_name = "Temoignage"
        verbose_name_plural = "Temoignages"

    nom = models.CharField(max_length=100)
    fonction = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='temoignages/')
    message = models.TextField()

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} - {self.fonction}"   
    
