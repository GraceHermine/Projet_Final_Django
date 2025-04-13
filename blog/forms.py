from django import forms
from Ecommerce.models import Blog


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["titre", "image", "description", "contenu", "categorie"]