from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Categorie,SousCategorie,Produit,Panier,PanierItem,Commande,Facture,Coupon,Expedition,Favoris,Tags,Paiement,Avis,Livreur
from django.utils.html import format_html
# Register your models here.



class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'nom', 'prenom', 'genre', 'datenaiss', 'numero', 'statut']
    search_fields = ['email', 'nom', 'prenom']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('nom', 'prenom', 'genre', 'datenaiss', 'numero', 'adresse', 'photo')}),
        ('Autres infos', {'fields': ('panier', 'statut')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'prenom', 'genre', 'datenaiss', 'numero', 'adresse', 'photo', 'panier', 'statut', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(User, CustomUserAdmin)



class CategorieAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('nom', 'description')
        }),
        ('Statut', {
            'fields': ('statut',)
        }),
    )
    list_display = ('nom', 'description', 'statut')
    list_filter = ('statut',)
    search_fields = ('nom', 'description')
    ordering = ('nom',)
    list_per_page = 10

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Categorie, CategorieAdmin)



class SousCategorieAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('nom', 'description', 'categorie')
        }),
        ('Statut', {
            'fields': ('statut',)
        }),
    )
    list_display = ('nom', 'description', 'categorie', 'statut')
    list_filter = ('statut', 'categorie')
    search_fields = ('nom', 'description')
    ordering = ('nom',)
    list_per_page = 10

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(SousCategorie, SousCategorieAdmin)




class ProduitAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('nom', 'description', 'prix', 'prix_promo', 'quantite', 'image', 'souscategorie')
        }),
        ('Options', {
            'fields': ('statut', 'pour_slider', 'en_promotion')
        }),
    )

    list_display = (
        'nom', 'souscategorie', 'prix', 'affiche_prix_promo', 
        'quantite', 'statut', 'en_promotion', 'pour_slider', 'apercu_image'
    )

    list_filter = ('statut', 'souscategorie', 'en_promotion', 'pour_slider')
    search_fields = ('nom', 'description')
    ordering = ('nom',)
    list_per_page = 10

    actions = ['active', 'desactive', 'mettre_en_promo', 'retirer_promo']

    def affiche_prix_promo(self, obj):
        if obj.en_promotion and obj.prix_promo:
            return f"{obj.prix_promo} €"
        return "-"
    affiche_prix_promo.short_description = "Prix promo"

    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;"/>', obj.image.url)
        return "-"
    apercu_image.short_description = "Image"

    def active(self, request, queryset):
        queryset.update(statut=True)
        self.message_user(request, "Les produits sélectionnés ont été activés.")
    active.short_description = "Activer"

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, "Les produits sélectionnés ont été désactivés.")
    desactive.short_description = "Désactiver"

    def mettre_en_promo(self, request, queryset):
        queryset.update(en_promotion=True)
        self.message_user(request, "Les produits sont maintenant en promotion.")
    mettre_en_promo.short_description = "Mettre en promotion"

    def retirer_promo(self, request, queryset):
        queryset.update(en_promotion=False, prix_promo=None)
        self.message_user(request, "Les produits ne sont plus en promotion.")
    retirer_promo.short_description = "Retirer de la promotion"

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Produit, ProduitAdmin)




class PanierAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('utilisateur', 'reduction', 'prixTotal')
        }),
        ('Statut', {
            'fields': ('statut',)
        }),
    )
    list_display = ('utilisateur', 'reduction', 'prixTotal', 'statut')
    list_filter = ('statut',)
    search_fields = ('utilisateur__nom', 'utilisateur__prenom')
    ordering = ('-created_at',)
    list_per_page = 10
    date_hierarchy = 'created_at'

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Panier, PanierAdmin)



class PanierItemAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('panier', 'produit', 'quantite', 'total')
        }),
        ('Statut', {
            'fields': ('statut',)
        }),
    )
    list_display = ('panier', 'produit', 'quantite','total', 'statut')
    list_filter = ('statut',)
    search_fields = ('panier', 'produit')
    ordering = ('-created_at',)
    list_per_page = 10
    date_hierarchy = 'created_at'

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(PanierItem, PanierItemAdmin)




class CommandeAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('utilisateur', 'prixtotal', 'inorder', 'accepted', 'deliver', 'fichierFacture')
        }),
        ('Statut', {
            'fields': ('statut',)
        }),
    )
    list_display = ('utilisateur', 'prixtotal', 'inorder', 'accepted', 'deliver', 'statut')
    list_filter = ('inorder', 'accepted', 'deliver', 'statut')
    search_fields = ('utilisateur__nom', 'utilisateur__prenom', 'prixtotal')
    ordering = ('-created_at',)
    list_per_page = 10
    date_hierarchy = 'created_at'

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Commande, CommandeAdmin)



class FactureAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('commande', 'created_at', 'montant', 'taxes')
        }),
        ('Statut', {
            'fields': ('statut',)
        }),
    )
    list_display = ('commande','montant', 'created_at', 'statut')
    list_filter = ('statut',)
    search_fields = ('commande', 'montant')
    ordering = ('-created_at',)
    list_per_page = 10
    date_hierarchy = 'created_at'

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Facture, FactureAdmin)



class CouponAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('code', 'valeur', 'expiration')
        }),
    )
    list_display = ('code', 'valeur', 'expiration')
    list_filter = ('expiration',)
    search_fields = ('code',)
    ordering = ('expiration',)
    list_per_page = 10

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Coupon, CouponAdmin)



class ExpeditionAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('commande', 'dateExpedition', 'adresse', 'statut')
        }),
    )
    list_display = ('commande', 'dateExpedition', 'adresse', 'statut')
    list_filter = ('statut',)
    search_fields = ('commande', 'adresse')
    ordering = ('-created_at',)
    list_per_page = 10
    date_hierarchy = 'created_at'


    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Expedition, ExpeditionAdmin)



class FavorisAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('utilisateur', 'produit')
        }),
    )
    list_display = ('utilisateur', 'produit')
    list_filter = ('utilisateur', 'produit')
    search_fields = ('utilisateur__nom', 'produit__nom')
    ordering = ('utilisateur',)
    list_per_page = 10

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Favoris, FavorisAdmin)




class TagsAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('titre',)
        }),
        ('Statut', {
            'fields': ('statut',)
        }),
    )
    list_display = ('titre', 'statut')
    list_filter = ('statut',)
    search_fields = ('titre',)
    ordering = ('titre',)
    list_per_page = 10

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Tags, TagsAdmin)



class PaiementAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('methode', 'montant', 'status')
        }),
        ('Statut', {
            'fields': ('statut',)
        }),
    )
    list_display = ('methode', 'montant', 'status', 'statut')
    list_filter = ('statut',)
    search_fields = ('methode', 'status')
    ordering = ('-created_at',)
    list_per_page = 10

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Paiement, PaiementAdmin)



class AvisAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('user', 'Produit', 'note', 'commentaire')
        }),
        ('Statut', {
            'fields': ('statut',)
        }),
    )
    list_display = ('user', 'Produit', 'note', 'statut')
    list_filter = ('statut', 'note')
    search_fields = ('User__nom', 'Produit__nom', 'commentaire')
    ordering = ('-created_at',)
    list_per_page = 10

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Avis, AvisAdmin)


class LivreurAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('nom', 'prenom', 'email', 'genre', 'langue', 'datenaiss', 'numero', 'adresse', 'photo', 'experience', 'competence')
        }),
        ('Statut', {
            'fields': ('statut',)
        }),
    )
    list_display = ('nom', 'prenom', 'email', 'genre', 'langue', 'statut')
    list_filter = ('genre', 'langue', 'statut')
    search_fields = ('nom', 'prenom', 'email')
    ordering = ('-created_at',)
    list_per_page = 10

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Livreur, LivreurAdmin)


admin.site.site_header = "Gestion E-commerce 🚀"
admin.site.site_title = "Admin - Boutique en ligne 🛒"
admin.site.index_title = "Bienvenue sur l'interface d'administration 📊"