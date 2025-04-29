from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import CustomUserCreationForm, ProfilUtilisateurForm
from .models import ProfilUtilisateur, ObjetConnecte, HistoriqueUtilisation
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from datetime import datetime, time
from django.contrib.auth import update_session_auth_hash


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

def reglement(request):
    return render(request, 'reglement.html')

def horaires(request):
    return render(request, 'horaires.html')

def detail_objet(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, pk=objet_id)

    if request.method == 'POST':
        objet.nom = request.POST.get('nom')
        objet.etat = request.POST.get('etat')
        objet.zone = request.POST.get('zone')
        objet.statut = request.POST.get('statut')
        heure_debut = request.POST.get('heure_debut_utilisation')
        heure_fin = request.POST.get('heure_fin_utilisation')

        if heure_debut:
            h, m = map(int, heure_debut.split(":"))
            objet.heure_debut_utilisation = time(h, m)
        else:
            objet.heure_debut_utilisation = None

        if heure_fin:
            h, m = map(int, heure_fin.split(":"))
            objet.heure_fin_utilisation = time(h, m)
        else:
            objet.heure_fin_utilisation = None
        objet.save()
        return redirect('objets_connectes')  # Après modification, retour vers la liste des objets

    return render(request, 'detail_objet.html', {'objet': objet})

def ajouter_objet(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        attribut = request.POST.get('attribut')
        zone = request.POST.get('zone')
        etat = request.POST.get('etat')
        statut = request.POST.get('statut')
        connectivite = request.POST.get('connectivite')
        marque = request.POST.get('marque')
        couleur = request.POST.get('couleur')
        annee_fin = request.POST.get('annee_fin')
        image = request.POST.get('image')

        # Définir l'année d'achat automatiquement
        annee_achat = datetime.now().year

        nouvel_objet = ObjetConnecte(
            nom=nom,
            attribut=attribut,
            zone=zone,
            etat=etat,
            statut=statut,
            connectivite=connectivite,
            marque=marque,
            couleur=couleur,
            annee_achat=annee_achat,
            annee_fin=annee_fin,
            image=image
        )
        nouvel_objet.save()
        messages.success(request, "Objet ajouté avec succès !")
        return redirect('objets_connectes')

    return render(request, 'ajouter_objet.html')


def visite(request):
    objets = ObjetConnecte.objects.all()
    # Si utilisateur connecté : recherche par mot-clé
    if request.user.is_authenticated:
        query = request.GET.get('q')
        if query:
            filtres = Q(nom__icontains=query) | Q(type__icontains=query) | Q(etat__icontains=query) | \
                      Q(zone__icontains=query) | Q(connectivite__icontains=query) | Q(marque__icontains=query) | \
                      Q(statut__icontains=query) | Q(couleur__icontains=query) | Q(attribut__icontains=query) | \
                      Q(intensite__icontains=query)

            try:
                # si la recherche est un nombre (int ou float), on l'inclut aussi dans les champs numériques
                num = float(query)
                filtres |= Q(vitesse_max=num) | Q(duree_max_jour=num)
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

def rapport_utilisation(request):
    historique = HistoriqueUtilisation.objects.all().order_by('-date')
    return render(request, 'rapport_utilisation.html', {'historique': historique})

def historique_objet(request, objet_id):
    historique = HistoriqueUtilisation.objects.filter(objet_id=objet_id).order_by('-date')
    return render(request, 'historique_objet.html', {'historique': historique})

def info_objet(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, id=objet_id)
    return render(request, 'info_objet.html', {'objet': objet})


@login_required
def profil(request):
    profil, _ = ProfilUtilisateur.objects.get_or_create(user=request.user)
    edit_mode = request.GET.get('edit') == '1'
    utilisateurs = ProfilUtilisateur.objects.select_related('user').all()


    if request.method == 'POST':
        form = ProfilUtilisateurForm(request.POST, request.FILES, instance=profil, user=request.user)
        if form.is_valid():
            form.save()

            # ✅ Gestion du changement de mot de passe
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            if new_password1 and new_password1 == new_password2:
                request.user.set_password(new_password1)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Important pour ne pas déconnecter l'utilisateur
                messages.success(request, "Mot de passe mis à jour avec succès.")

            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('profil')
    else:
        form = ProfilUtilisateurForm(instance=profil, user=request.user)

    return render(request, 'profil.html', {
        'form': form,
        'profil': profil,
        'edit': edit_mode,
        'utilisateurs': utilisateurs, 
    })


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# ============ SYSTEME DE POINTS AUTOMATIQUE =============

def ajouter_points(request, points, cle_session):
    if request.user.is_authenticated:
        profil, _ = ProfilUtilisateur.objects.get_or_create(user=request.user)
        if not request.session.get(cle_session):  # Évite d'ajouter les mêmes points plusieurs fois
            profil.points += points
            profil.save()
            request.session[cle_session] = True
            verifier_niveau(profil)

def verifier_niveau(profil):
    """ Met automatiquement à jour le niveau selon les nouveaux points """
    p = profil.points
    if p >= 7 and profil.niveau_experience != 'expert':
        profil.niveau_experience = 'expert'
        profil.user.is_staff = True  # ✅ Devient admin Django
        profil.user.save()
    elif p >= 5 and profil.niveau_experience != 'avancé':
        profil.niveau_experience = 'avancé'
    elif p >= 3 and profil.niveau_experience != 'intermédiaire':
        profil.niveau_experience = 'intermédiaire'
    else:
        profil.niveau_experience = 'débutant'
    
    profil.save()


# ===================== FONCTIONNALITÉS ====================

@login_required
def objets_connectes(request):
    ajouter_points(request, 2, 'visited_objets')
    objets = ObjetConnecte.objects.all()
    return render(request, 'objets_connectes.html', {'objets': objets})

@login_required
def performances(request):
    ajouter_points(request, 2, 'visited_performance')
    return render(request, 'performances.html')

@login_required
def personnalisation(request):
    ajouter_points(request, 2, 'visited_perso')
    return render(request, 'personnalisation.html')
