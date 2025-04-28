from django.db import models
from django.contrib.auth.models import User

class ProfilUtilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sexe = models.CharField(max_length=10, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    niveau_experience = models.CharField(max_length=50, default='débutant')
    photo_profil = models.ImageField(upload_to='photos_profil/', null=True, blank=True)
    points = models.IntegerField(default=1)  # Débutant a 1 point par défaut


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

TYPE_CHOICES = [
    ('tapis', 'Tapis de course'),
    ('stepper', 'Stepper'),
    ('velo', 'Vélo'),
    ('rameur', 'Rameur'),
    ('elliptique', 'Elliptique'),
]

ZONE_CHOICES = [
    ('cardio', 'Zone Cardio'),
    ('ambiance', 'Zone Ambiance'),
]

STATUT_CHOICES = [
    ('actif', 'Actif'),
    ('panne', 'Panne'),
    ('maintenance', 'Maintenance'),
]

ETAT_CHOICES = [
    ('neuf', 'Neuf'),
    ('tres_bon', 'Très bon état'),
    ('bon', 'Bon état'),
    ('moyen', 'État moyen'),
    ('mauvais', 'Mauvais état'),
]

class ObjetConnecte(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    etat = models.CharField(max_length=50, choices=ETAT_CHOICES)
    zone = models.CharField(max_length=50, choices=ZONE_CHOICES)
    annee_achat = models.IntegerField(null=True, blank=True)
    annee_fin = models.IntegerField(null=True, blank=True)
    attribut = models.TextField(blank=True, null=True)
    connectivite = models.CharField(max_length=100)
    couleur = models.CharField(max_length=50, null=True, blank=True)
    derniere_maintenance = models.DateField(null=True, blank=True)
    duree_max_jour = models.IntegerField(null=True, blank=True)
    est_disponible = models.BooleanField(default=True)
    image = models.URLField(max_length=300, null=True, blank=True)
    inclinaison_max = models.CharField(max_length=50, null=True, blank=True)
    marque = models.CharField(max_length=100)
    puissance = models.CharField(max_length=50, null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
    vitesse_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    intensite = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.get_type_display()})"

class HistoriqueUtilisation(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    objet = models.ForeignKey(ObjetConnecte, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.objet.nom} - {self.action}"
