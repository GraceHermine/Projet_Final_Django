from django.contrib import admin
from .models import Blog, Commentaire
# Register your models here.
class BlogAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('auteur', 'image', 'titre', 'description', 'categorie', 'contenu')
        }),
        ('Statut', {
            'fields': ('statut', 'slug')
        }),
    )
    list_display = ('titre', 'auteur', 'categorie', 'cartepublication', 'statut')
    list_display_links = ('titre',)
    list_filter = ('categorie', 'statut')
    search_fields = ('titre', 'description', 'contenu')
    ordering = ('-cartepublication',)
    list_per_page = 10
    date_hierarchy = 'cartepublication'

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

_register(Blog, BlogAdmin)



class CommentaireAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('blog', 'utilisateur', 'titre', 'contenu')
        }),
        ('Statut', {
            'fields': ('statut',)
        }),
    )
    list_display = ('blog', 'utilisateur', 'titre', 'statut')
    list_filter = ('statut',)
    search_fields = ('titre', 'contenu')
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

_register(Commentaire, CommentaireAdmin)

