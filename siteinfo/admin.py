from django.contrib import admin
from .models import Faq,Equipe,Politique,Propos,Temoignage,Conditions
# Register your models here.


class FaqAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('question', 'reponse')
        }),
        ('Statut', {
            'fields': ('statut',)
        }),
    )
    list_display = ('question','reponse', 'statut')
    list_filter = ('statut',)
    search_fields = ('question', 'statut')
    ordering = ('question',)
    list_per_page = 10

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La question a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La question a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Faq, FaqAdmin)



class PolitiqueAdmin(admin.ModelAdmin):
    list_display = ('titre', 'statut', 'last_updated_at')
    list_filter = ('statut',)
    search_fields = ('titre',)
    ordering = ('-last_updated_at',)
    list_per_page = 10
    
    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La question a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La question a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Politique, PolitiqueAdmin)



class ConditionsAdmin(admin.ModelAdmin):
    list_display = ('titre', 'statut', 'created_at')
    search_fields = ('titre',)
    list_filter = ('statut',)
    ordering = ('-created_at',)

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La question a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La question a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Conditions, ConditionsAdmin)



class ProposAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('titre', 'description', 'image', 'soustitre', 'contenu', 'photo', 'nom', 'histore',  'portrait', 'statut')
        }),
        ('Dates', {
            'fields': ('created_at', 'last_updated_at'),
            'classes': ('collapse',)
        }),
    )
    list_display = ('titre', 'soustitre', 'statut', 'created_at', 'last_updated_at')
    list_filter = ('statut',)
    search_fields = ('titre', 'soustitre')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'last_updated_at')

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La question a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La question a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Propos, ProposAdmin)


class EquipeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'poste', 'statut')
    list_filter = ('statut',)
    search_fields = ('nom', 'poste', 'email')
    ordering = ('nom',)  

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La question a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La question a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Equipe, EquipeAdmin)



class TemoinAdmin(admin.ModelAdmin):
    list_display = ('nom', 'fonction', 'photo', 'message', 'statut')
    list_filter = ('statut',)
    search_fields = ('nom', 'statut', 'fonction')
    ordering = ('nom',)  

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La question a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La question a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Temoignage, TemoinAdmin)
