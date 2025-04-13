
from rest_framework import viewsets,  permissions
from api.serializers import *
from blog.models import Blog,Commentaire
from siteinfo.models import Faq, Politique, Propos,Conditions, Equipe, Temoignage 
from Ecommerce.models import *


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.filter(statut=True)
    serializer_class = BlogSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)


class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.filter(statut=True)
    serializer_class = CommentaireSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)



class FaqViewSet(viewsets.ModelViewSet):
    queryset = Faq.objects.filter(statut=True)
    serializer_class = FaqSerializer
    permission_classes = [permissions.IsAuthenticated]

class PolitiqueViewSet(viewsets.ModelViewSet):
    queryset = Politique.objects.filter(statut=True)
    serializer_class = PolitiqueSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConditionsViewSet(viewsets.ModelViewSet):
    queryset = Conditions.objects.filter(statut=True)
    serializer_class = ConditionsSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProposViewSet(viewsets.ModelViewSet):
    queryset = Propos.objects.filter(statut=True)
    serializer_class = ProposSerializer
    permission_classes = [permissions.IsAuthenticated]

class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.filter(statut=True)
    serializer_class = EquipeSerializer
    permission_classes = [permissions.IsAuthenticated]

class TemoignageViewSet(viewsets.ModelViewSet):
    queryset = Temoignage.objects.filter(statut=True)
    serializer_class = TemoignageSerializer
    permission_classes = [permissions.IsAuthenticated]




class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.filter(statut=True)
    serializer_class = CategorieSerializer
    permission_classes = [permissions.IsAuthenticated]

class SousCategorieViewSet(viewsets.ModelViewSet):
    queryset = SousCategorie.objects.filter(statut=True)
    serializer_class = SousCategorieSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.filter(statut=True)
    serializer_class = ProduitSerializer
    permission_classes = [permissions.IsAuthenticated]

class PanierViewSet(viewsets.ModelViewSet):
    queryset = Panier.objects.filter(statut=True)
    serializer_class = PanierSerializer
    permission_classes = [permissions.IsAuthenticated]

class PanierItemViewSet(viewsets.ModelViewSet):
    queryset = PanierItem.objects.filter(statut=True)
    serializer_class = PanierItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.filter(statut=True)
    serializer_class = CommandeSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommandeItemViewSet(viewsets.ModelViewSet):
    queryset = CommandeItem.objects.all()
    serializer_class = CommandeItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class FactureViewSet(viewsets.ModelViewSet):
    queryset = Facture.objects.all()
    serializer_class = FactureSerializer
    permission_classes = [permissions.IsAuthenticated]

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.filter(statut=True)
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExpeditionViewSet(viewsets.ModelViewSet):
    queryset = Expedition.objects.filter(statut=True)
    serializer_class = ExpeditionSerializer
    permission_classes = [permissions.IsAuthenticated]

class FavorisViewSet(viewsets.ModelViewSet):
    queryset = Favoris.objects.filter(statut=True)
    serializer_class = FavorisSerializer
    permission_classes = [permissions.IsAuthenticated]

class AvisViewSet(viewsets.ModelViewSet):
    queryset = Avis.objects.filter(statut=True)
    serializer_class = AvisSerializer
    permission_classes = [permissions.IsAuthenticated]

class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.filter(statut=True)
    serializer_class = TagsSerializer
    permission_classes = [permissions.IsAuthenticated]

class LivreurViewSet(viewsets.ModelViewSet):
    queryset = Livreur.objects.filter(statut=True)
    serializer_class = LivreurSerializer
    permission_classes = [permissions.IsAuthenticated]