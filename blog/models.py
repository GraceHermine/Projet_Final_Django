from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from Ecommerce.models import User, Categorie

# Create your models here.


# Il bouge aussi
class Blog(models.Model):

    class Meta:
        app_label = 'Ecommerce'
        verbose_name = "Blog"
        verbose_name_plural = "Blog"
    
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    cartepublication = models.DateTimeField(auto_now_add=True)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="categorie_blog")
    contenu = CKEditor5Field('Text', config_name='extends')
    slug = models.SlugField(unique=True, blank=True, null=True) 


    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre
    

# Il bouge aussi
class Commentaire(models.Model):

    class Meta:
        app_label = 'Ecommerce'
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
    
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="reponses")

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre
  