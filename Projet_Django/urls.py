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

    # ✅ Ajout des vues pour le système de points
    path('objets-connectes/', views.objets_connectes, name='objets_connectes'),
    path('performances/', views.performances, name='performances'),
    path('personnalisation/', views.personnalisation, name='personnalisation'),
    path('objectif/', views.objectif, name='objectif'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
