from django.contrib import admin
from django.urls import path
from App_django_ConnectedGym import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.acceuil, name='acceuil'),  # racine = page d'accueil
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('equipe/', views.equipe, name='equipe'),
    path('visite/', views.visite, name='visite'),


]
