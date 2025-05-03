from django.contrib import admin, messages
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, redirect
from .models import (
    ProfilUtilisateur,
    ObjetConnecte,
    HistoriqueUtilisation,
    DemandeSuppressionObjet
)

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

@admin.register(DemandeSuppressionObjet)
class DemandeSuppressionAdmin(admin.ModelAdmin):
    list_display = ('objet', 'utilisateur', 'date_demande', 'traite', 'valider_et_supprimer_lien')
    list_filter = ('traite',)
    search_fields = ('objet__nom', 'utilisateur__username')
    actions = ['valider_et_supprimer_objet']

    # Bouton cliquable par ligne dans le tableau admin
    def valider_et_supprimer_lien(self, obj):
        if not obj.traite:
            return format_html(
                '<a class="button" href="{}">Valider et supprimer</a>',
                reverse('admin:valider_suppression_objet', args=[obj.id])
            )
        return "Déjà traité"
    valider_et_supprimer_lien.short_description = "Action"

    # Action groupée sur plusieurs lignes sélectionnées
    @admin.action(description="Valider les demandes et supprimer les objets")
    def valider_et_supprimer_objet(self, request, queryset):
        for demande in queryset:
            if not demande.traite:
                objet_nom = str(demande.objet)
                demande.objet.delete()
                demande.traite = True
                demande.save(update_fields=["traite"])
        self.message_user(request, "Les objets sélectionnés ont été supprimés avec succès.")

    # Routes personnalisées admin
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'valider-suppression/<int:demande_id>/',
                self.admin_site.admin_view(self.valider_suppression_objet),
                name='valider_suppression_objet',
            ),
        ]
        return custom_urls + urls

    # Vue appelée par le bouton personnalisé
    def valider_suppression_objet(self, request, demande_id):
        demande = DemandeSuppressionObjet.objects.filter(id=demande_id).first()
        if not demande:
            self.message_user(request, "Cette demande n'existe pas.", level=messages.ERROR)
            return redirect('admin:App_django_ConnectedGym_demandesuppressionobjet_changelist')

        if not demande.traite:
            objet = demande.objet  # stocker avant suppression
            objet_nom = str(objet)
            objet.delete()
            demande.traite = True
            demande.save(update_fields=["traite"])
            self.message_user(request, f"L'objet « {objet_nom} » a été supprimé avec succès.")
        else:
            self.message_user(request, "Cette demande a déjà été traitée.", level=messages.WARNING)

        return redirect('admin:App_django_ConnectedGym_demandesuppressionobjet_changelist')
