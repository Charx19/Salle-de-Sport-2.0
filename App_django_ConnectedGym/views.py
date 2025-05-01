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
from .models import ZONE_CHOICES, ETAT_CHOICES, STATUT_CHOICES
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from datetime import datetime, time
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
import matplotlib.pyplot as plt
import io
import base64
from django.db import IntegrityError


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

TYPES_CHOICE = ["Tapis de course", "Stepper", "Vélo", "Rameur", "Elliptique"]

from datetime import datetime, time

@login_required
def modif_objet(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, pk=objet_id)

    if request.method == 'POST':
        print("Formulaire POST reçu")
        print("Données reçues:", request.POST)  # Debug
        
        # Champs de base
        objet.nom = request.POST.get('nom', objet.nom)
        objet.etat = request.POST.get('etat', objet.etat)
        objet.zone = request.POST.get('zone', objet.zone)
        objet.marque = request.POST.get('marque', objet.marque)
        objet.annee_fin = request.POST.get('annee_fin', objet.annee_fin)
        
        # Champs spécifiques
        objet.type_transmission = request.POST.get("type_transmission", objet.type_transmission)
        objet.type_resistance = request.POST.get("type_resistance") or \
                  request.POST.get("type_resistance_r") or None
        objet.intensite = request.POST.get("intensite") or \
                  request.POST.get("intensite_v") or \
                  request.POST.get("intensite_s") or \
                  request.POST.get("intensite_r") or \
                  request.POST.get("intensite_e") or None
        objet.vitesse_max = request.POST.get("vitesse_max") or \
                  request.POST.get("vitesse_max_v") or \
                  request.POST.get("vitesse_max_s") or \
                  request.POST.get("vitesse_max_r") or \
                  request.POST.get("vitesse_max_e") or None
        objet.puissance = request.POST.get("puissance") or \
                  request.POST.get("puissance_v") or \
                  request.POST.get("puissance_s") or \
                  request.POST.get("puissance_r") or \
                  request.POST.get("puissance_e") or None

        objet.inclinaison_max = request.POST.get("inclinaison_max") or \
                  request.POST.get("inclinaison_max_v") or \
                  request.POST.get("inclinaison_max_s") or \
                  request.POST.get("inclinaison_max_r") or \
                  request.POST.get("inclinaison_max_e") or None
        
        objet.amorti = request.POST.get("amorti", objet.amorti)
        objet.ventilation_frontale = any([
            request.POST.get("vf") == "on",
            request.POST.get("vf_") == "on"
        ])

        objet.hauteur_marche = request.POST.get("hauteur_marche", objet.hauteur_marche)
        objet.longueur_pas = request.POST.get("longueur_pas", objet.longueur_pas)
        objet.longueur_rail = request.POST.get("longueur_rail", objet.longueur_rail)
        objet.type_mouvement = request.POST.get("type_mouvement", objet.type_mouvement)

        # Gestion du statut
        ancien_statut = objet.statut
        nouvel_statut = request.POST.get('statut', objet.statut)
        objet.statut = nouvel_statut

        if ancien_statut != "maintenance" and nouvel_statut == "maintenance":
            objet.derniere_maintenance = datetime.today().date()

        try:
            objet.save()
            try:
                HistoriqueUtilisation.objects.create(
                    objet=objet,
                    utilisateur=request.user,
                    action="modifié",
                    vitesse_max=objet.vitesse_max,
                    puissance=objet.puissance,
                    inclinaison_max=objet.inclinaison_max,
                    intensite=objet.intensite,
                    amorti=objet.amorti,
                    ventilation_frontale=objet.ventilation_frontale,
                    hauteur_marche=objet.hauteur_marche,
                    longueur_rail=objet.longueur_rail,
                    longueur_pas=objet.longueur_pas,
                    type_transmission=objet.type_transmission,
                    type_resistance=objet.type_resistance,
                    type_mouvement=objet.type_mouvement
                )
                print("Historique enregistré avec succès")
            except IntegrityError:
                messages.error(request, "Erreur lors de l'enregistrement de l'historique. Vérifiez les données.")
            except Exception as e:
                print(f"Erreur lors de l'enregistrement de l'historique: {str(e)}")

            messages.success(request, "Modifications enregistrées avec succès")
            return redirect('objets_connectes')
        except Exception as e:
            messages.error(request, f"Erreur lors de la sauvegarde: {str(e)}")
            return render(request, 'modif_objet.html', {
                'objet': objet,
                'zone_choices': ZONE_CHOICES,
                'etat_choices': ETAT_CHOICES,
                'statut_choices': STATUT_CHOICES,
            })

    return render(request, 'modif_objet.html', {
        'objet': objet,
        'zone_choices': ZONE_CHOICES,
        'etat_choices': ETAT_CHOICES,
        'statut_choices': STATUT_CHOICES,
    })



@login_required
def ajouter_objet(request):
    if request.method == 'POST':
        type_choisi = request.POST.get('type')
        if type_choisi not in TYPES_CHOICE:
            messages.error(request, "Type non autorisé.")
            return redirect('ajouter_objet')

        # Champs généraux
        nom = request.POST.get('nom')
        attribut = request.POST.get('attribut')
        zone = request.POST.get('zone')
        etat = request.POST.get('etat')
        statut = request.POST.get('statut')
        connectivite = request.POST.get('connectivite')
        marque = request.POST.get('marque')
        couleur = request.POST.get('couleur')
        annee_fin = request.POST.get('annee_fin')
        image = request.FILES.get('image')
        annee_achat = datetime.now().year

        # Champs spécifiques selon les types
        intensite = request.POST.get('intensite')
        puissance = request.POST.get('puissance')
        vitesse_max = request.POST.get('vitesse_max')
        inclinaison_max = request.POST.get('inclinaison_max')
        hauteur_marche = request.POST.get('hauteur_marche')
        longueur_rail = request.POST.get('longueur_rail')
        longueur_pas = request.POST.get('longueur_pas')
        type_mouvement = request.POST.get('type_mouvement')
        type_transmission = request.POST.get('type_transmission')
        type_resistance = request.POST.get('type_resistance') or request.POST.get('type_resistance_r')
        amorti = request.POST.get('amorti')
        ventilation_frontale = request.POST.get('vf') == "on" or request.POST.get('vf_') == "on"
        est_disponible = True
        nouvel_objet = ObjetConnecte(
            nom=nom,
            type=type_choisi.lower(),
            attribut=attribut,
            zone=zone,
            etat=etat,
            statut=statut,
            connectivite=connectivite,
            marque=marque,
            couleur=couleur,
            annee_achat=annee_achat,
            annee_fin=annee_fin,
            image=image,
            intensite=intensite,
            puissance=puissance,
            vitesse_max=vitesse_max,
            inclinaison_max=inclinaison_max,
            hauteur_marche=hauteur_marche,
            longueur_rail=longueur_rail,
            longueur_pas=longueur_pas,
            type_mouvement=type_mouvement,
            type_transmission=type_transmission,
            type_resistance=type_resistance,
            amorti=amorti,
            ventilation_frontale=ventilation_frontale,
            est_disponible=est_disponible,
        )

        nouvel_objet.save()
        messages.success(request, "Objet ajouté avec succès !")
        return redirect('objets_connectes')

    return render(request, 'ajouter_objet.html', {'types_autorises': TYPES_CHOICE})



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



def historique_objet(request, objet_id):
    historique = HistoriqueUtilisation.objects.filter(objet_id=objet_id).order_by('-date')

    def plot_to_base64(dates, valeurs, label, unit):
        if len(dates) != len(valeurs):
            return None
        fig, ax = plt.subplots(figsize=(8, 4))  # Largeur et hauteur améliorées

        ax.plot(dates, valeurs, marker='o', linestyle='-', color='tab:blue')
        ax.set_title(f"Évolution de {label}", fontsize=14)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel(f"{label} ({unit})", fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.tick_params(axis='both', labelsize=10)
        ax.grid(True)
        fig.tight_layout()  # Corrige les débordements

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')
        encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
        plt.close(fig)
        return f"data:image/png;base64,{encoded}"


    # Données séparées
    dates_v = []
    valeurs_v = []
    dates_p = []
    valeurs_p = []
    dates_i = []
    valeurs_i = []

    for h in historique:
        if h.vitesse_max is not None:
            dates_v.append(h.date)
            valeurs_v.append(float(h.vitesse_max))
        if h.puissance is not None:
            dates_p.append(h.date)
            valeurs_p.append(float(h.puissance))
        if h.inclinaison_max is not None:
            try:
                valeurs_i.append(float(h.inclinaison_max))
                dates_i.append(h.date)
            except ValueError:
                continue

    graph_vitesse = plot_to_base64(dates_v, valeurs_v, "Vitesse", "km/h") if valeurs_v else None
    graph_puissance = plot_to_base64(dates_p, valeurs_p, "Puissance", "W") if valeurs_p else None
    graph_inclinaison = plot_to_base64(dates_i, valeurs_i, "Inclinaison", "%") if valeurs_i else None

    return render(request, 'historique_objet.html', {
        'historique': historique,
        'graph_vitesse': graph_vitesse,
        'graph_puissance': graph_puissance,
        'graph_inclinaison': graph_inclinaison,
    })




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

@login_required
def demander_suppression(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, pk=objet_id)

    # Ici, on pourrait enregistrer la demande dans une table dédiée
    # ou envoyer un mail à un admin. Pour l'instant, on marque l'objet comme "en attente de suppression"
    objet.statut = "suppression_demande"
    objet.save()

    messages.success(request, f"La demande de suppression pour « {objet.nom} » a été enregistrée.")
    return redirect('objets_connectes')
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
