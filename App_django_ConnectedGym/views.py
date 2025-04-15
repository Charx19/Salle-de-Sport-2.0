from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import CustomUserCreationForm, ProfilUtilisateurForm
from .models import ProfilUtilisateur

def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue {user.first_name} ! Vous êtes maintenant inscrit et connecté.")
            return redirect('acceuil')
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
    return redirect('acceuil')


def equipe(request):
    return render(request, 'equipe.html')


def visite(request):
    return render(request, 'visite.html')


@login_required
def profil(request):
    profil, _ = ProfilUtilisateur.objects.get_or_create(user=request.user)
    edit_mode = request.GET.get('edit') == '1'

    if request.method == 'POST':
        form = ProfilUtilisateurForm(request.POST, request.FILES, instance=profil, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('profil')
    else:
        form = ProfilUtilisateurForm(instance=profil, user=request.user)

    return render(request, 'profil.html', {
        'form': form,
        'profil': profil,
        'edit': edit_mode,
    })


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# ============ SYSTEME DE POINTS AUTOMATIQUE =============

def ajouter_points(request, points, cle_session):
    if request.user.is_authenticated:
        profil, _ = ProfilUtilisateur.objects.get_or_create(user=request.user)
        if not request.session.get(cle_session):  # Empêche d’ajouter deux fois les mêmes points
            profil.points += points
            profil.save()
            request.session[cle_session] = True
            verifier_niveau(profil)

def verifier_niveau(profil):
    """ Met automatiquement à jour le niveau selon les points """
    p = profil.points
    if p >= 7 and profil.niveau_experience != 'expert':
        profil.niveau_experience = 'expert'
        profil.user.is_staff = True  # ✅ devient admin Django
    elif p >= 5 and profil.niveau_experience != 'avancé':
        profil.niveau_experience = 'avancé'
    elif p >= 3 and profil.niveau_experience != 'intermédiaire':
        profil.niveau_experience = 'intermédiaire'
    elif p < 3:
        profil.niveau_experience = 'débutant'
    
    profil.save()

# ===================== FONCTIONNALITÉS ====================

@login_required
def objets_connectes(request):
    ajouter_points(request, 2, 'visited_objets')
    return render(request, 'objets_connectes.html')

@login_required
def performances(request):
    ajouter_points(request, 2, 'visited_performance')
    return render(request, 'performances.html')

@login_required
def personnalisation(request):
    ajouter_points(request, 2, 'visited_perso')
    return render(request, 'personnalisation.html')
