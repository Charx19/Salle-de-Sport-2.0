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

    def valider_et_supprimer_lien(self, obj):
        if not obj.traite:
            return format_html(
                '<a class="button" href="{}">Valider et supprimer</a>',
                reverse('admin:valider_suppression_objet', args=[obj.id])
            )
        return "Déjà traité"
    valider_et_supprimer_lien.short_description = "Action"

    @admin.action(description="Valider la demande et supprimer l'objet")
    def valider_et_supprimer_objet(self, request, queryset):
        for demande in queryset:
            if not demande.traite:
                # Stocker le nom avant suppression
                objet_nom = demande.objet.nom
                demande.objet.delete()
                # Utiliser update() pour éviter le problème d'objet supprimé
                DemandeSuppressionObjet.objects.filter(pk=demande.pk).update(traite=True)
        self.message_user(request, "Suppression(s) validée(s) avec succès.")

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

    def valider_suppression_objet(self, request, demande_id):
        demande = get_object_or_404(DemandeSuppressionObjet, id=demande_id)
        if not demande.traite:
            objet_nom = demande.objet.nom
            demande.objet.delete()
            # mise à jour sécurisée sans save()
            DemandeSuppressionObjet.objects.filter(pk=demande.pk).update(traite=True)
            self.message_user(request, f"L'objet « {objet_nom} » a été supprimé.")
        else:
            self.message_user(request, "Cette demande a déjà été traitée.", level=messages.WARNING)
        return redirect('admin:App_django_ConnectedGym_demandesuppressionobjet_changelist')
