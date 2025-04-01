from django.contrib import admin
from .models import ProfilUtilisateur, ObjetConnecte, HistoriqueUtilisation

@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('user', 'sexe', 'date_naissance', 'niveau_experience')
    search_fields = ('user__username', 'niveau_experience')

@admin.register(ObjetConnecte)
class ObjetConnecteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'etat')
    search_fields = ('nom', 'type')

@admin.register(HistoriqueUtilisation)
class HistoriqueUtilisationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'objet', 'date', 'action')
    search_fields = ('utilisateur__username', 'objet__nom', 'action')
    list_filter = ('date',)
