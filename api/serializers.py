from rest_framework import serializers
from blog.models import Blog, Commentaire
from Ecommerce.models import User, Categorie
from rest_framework import serializers
from siteinfo.models import Faq, Politique, Propos,Conditions, Equipe, Temoignage
from Ecommerce.models import *


class BlogSerializer(serializers.ModelSerializer):
    auteur = serializers.StringRelatedField()
    categorie = serializers.StringRelatedField()

    class Meta:
        model = Blog
        fields = '__all__'


class CommentaireSerializer(serializers.ModelSerializer):
    utilisateur = serializers.StringRelatedField()
    blog = serializers.StringRelatedField()

    class Meta:
        model = Commentaire
        fields = '__all__'




class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'

class PolitiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Politique
        fields = '__all__'

class ConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conditions
        fields = '__all__'

class ProposSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propos
        fields = '__all__'

class EquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = '__all__'

class TemoignageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temoignage
        fields = '__all__'




class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

class SousCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = SousCategorie
        fields = '__all__'

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'

class PanierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panier
        fields = '__all__'

class PanierItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanierItem
        fields = '__all__'

class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'

class CommandeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandeItem
        fields = '__all__'

class FactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facture
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class ExpeditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expedition
        fields = '__all__'

class FavorisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favoris
        fields = '__all__'

class AvisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avis
        fields = '__all__'

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class LivreurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livreur
        fields = '__all__'