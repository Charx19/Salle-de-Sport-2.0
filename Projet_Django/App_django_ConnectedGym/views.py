from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import CustomUserCreationForm

def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique après inscription
            messages.success(request, f"Bienvenue {user.first_name} ! Vous êtes maintenant inscrit et connecté.")
            return redirect('acceuil')  # Redirection vers l'accueil
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez vérifier le formulaire.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {user.first_name} ! Vous êtes connecté.")
            return redirect('acceuil')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'connexion.html')


def acceuil(request):
    return render(request, 'acceuil.html')

def deconnexion(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('acceuil')  # 👈 redirection vers l’accueil après déconnexion

def equipe(request):
    return render(request, 'equipe.html')

def visite(request):
    return render(request, 'visite.html')

def profil(request):
    return render(request, 'profil.html')

@login_required
def modifier_infos(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)
        user.save()
        messages.success(request, "Vos informations ont été mises à jour.")
        return redirect("profil")
