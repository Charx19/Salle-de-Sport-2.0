from django.contrib import admin
from django.urls import path
from App_django_ConnectedGym import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.acceuil, name='acceuil'),  # Page d'accueil
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('equipe/', views.equipe, name='equipe'),
    path('visite/', views.visite, name='visite'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profil/', views.profil, name='profil'),
    path('reglement/', views.reglement, name='reglement'),
    path('horaires/', views.horaires, name='horaires'),
    path('objet/<int:objet_id>/', views.detail_objet, name='detail_objet'),
    path('ajouter-objet/', views.ajouter_objet, name='ajouter_objet'),
    path('rapport-utilisation/', views.rapport_utilisation, name='rapport_utilisation'),
    path('historique-objet/<int:objet_id>/', views.historique_objet, name='historique_objet'),
    path('objets/', views.objets_connectes, name='objets_connectes'),

    path('activation/<uidb64>/<token>/', views.activation_compte, name='activation_compte'),

    # ✅ Ajout des vues pour le système de points
    path('objets-connectes/', views.objets_connectes, name='objets_connectes'),
    path('performances/', views.performances, name='performances'),
    path('personnalisation/', views.personnalisation, name='personnalisation'),
    path('objectif/', views.objectif, name='objectif'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
