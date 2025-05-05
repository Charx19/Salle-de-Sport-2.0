from django.contrib import admin, messages
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .views import mettre_a_jour_permissions_admin
from .models import (
    ProfilUtilisateur,
    ObjetConnecte,
    HistoriqueUtilisation,
    DemandeSuppressionObjet
)

# Permet de modifier le ProfilUtilisateur depuis l’admin User
class ProfilUtilisateurInline(admin.StackedInline):
    model = ProfilUtilisateur
    can_delete = False
    verbose_name_plural = 'Profil Utilisateur'
    fk_name = 'user'

# Customisation du UserAdmin avec le profil visible
class CustomUserAdmin(UserAdmin):
    inlines = (ProfilUtilisateurInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or (
            request.user.is_staff and hasattr(request.user, 'profilutilisateur')
            and request.user.profilutilisateur.niveau_experience == 'expert'
        ):
            return qs
        return qs.none()

# Remplacer l’admin standard de User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Admin du profil utilisateur (✅ avec mise à jour des points et permissions)
@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('user', 'sexe', 'date_naissance', 'niveau_experience', 'points')
    list_editable = ('niveau_experience',)
    search_fields = ('user__username', 'niveau_experience')
    list_filter = ('niveau_experience',)

    def save_model(self, request, obj, form, change):
        niveaux_points = {
            'débutant': 1,
            'intermédiaire': 3,
            'avancé': 7,
            'expert': 10
        }
        # Met à jour les points automatiquement
        obj.points = niveaux_points.get(obj.niveau_experience, obj.points)
        obj.save()

        # Met à jour les droits admin
        mettre_a_jour_permissions_admin(obj.user, obj.niveau_experience)

# Admin des objets connectés
@admin.register(ObjetConnecte)
class ObjetConnecteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'etat', 'est_disponible')
    search_fields = ('nom', 'type')

# Admin de l’historique d’utilisation
@admin.register(HistoriqueUtilisation)
class HistoriqueUtilisationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'objet', 'date', 'action')
    search_fields = ('utilisateur__username', 'objet__nom', 'action')
    list_filter = ('date',)

# Admin des demandes de suppression
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
                objet_nom = demande.objet.nom
                demande.objet.delete()
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
            DemandeSuppressionObjet.objects.filter(pk=demande.pk).update(traite=True)
            self.message_user(request, f"L'objet « {objet_nom} » a été supprimé.")
        else:
            self.message_user(request, "Cette demande a déjà été traitée.", level=messages.WARNING)
        return redirect('admin:App_django_ConnectedGym_demandesuppressionobjet_changelist')
