from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import CustomUserCreationForm, ProfilUtilisateurForm
from .models import ProfilUtilisateur, ObjetConnecte
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse

User = get_user_model()

# ============ VUES PRINCIPALES =============

def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activation de votre compte ConnectedGym'
            text_content = f"Bonjour {user.first_name}, veuillez cliquer sur le lien pour activer votre compte : http://{current_site.domain}{reverse('activation_compte', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': default_token_generator.make_token(user)})}"
            
            html_content = render_to_string('activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            
            email = EmailMultiAlternatives(subject, text_content, 'ConnectedGym <noreply@connectedgym.com>', [user.email])
            email.attach_alternative(html_content, "text/html")
            email.send()

            messages.success(request, "Inscription réussie ! Un email de confirmation vous a été envoyé.")
            return redirect('connexion')
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez vérifier le formulaire.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})


def activation_compte(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Votre compte a été activé avec succès. Vous pouvez maintenant vous connecter.')
        return redirect('connexion')
    else:
        messages.error(request, "Le lien d'activation est invalide ou a expiré.")
        return redirect('connexion')

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

def objectif(request):
    return render(request, 'objectif.html')

def visite(request):
    objets = ObjetConnecte.objects.all()
    # Si utilisateur connecté : recherche par mot-clé
    if request.user.is_authenticated:
        query = request.GET.get('q')
        if query:
            filtres = Q(nom__icontains=query) | Q(type__icontains=query) | Q(etat__icontains=query) | Q(zone__icontains=query) | \
                      Q(connectivite__icontains=query) | Q(marque__icontains=query) | Q(statut__icontains=query) | \
                      Q(couleur__icontains=query) | Q(attribut__icontains=query)

            try:
                # si la recherche est un nombre (int ou float), on l'inclut aussi dans les champs numériques
                num = float(query)
                filtres |= Q(capacite_max=num) | Q(precision=num) | Q(volume_max=num) | Q(intensite=num)
            except ValueError:
                pass

            objets = objets.filter(filtres)
    else:
        # Utilisateur non connecté : filtres doubles
        
        filtre_zone = request.GET.get("filtre1")  # ex: ambiance
        filtre_statut = request.GET.get("filtre2")  # ex: actif

        if filtre_zone and filtre_statut:
            objets = objets.filter(zone__iexact=filtre_zone, statut__iexact=filtre_statut)
    return render(request, 'visite.html', {'objets': objets})


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
