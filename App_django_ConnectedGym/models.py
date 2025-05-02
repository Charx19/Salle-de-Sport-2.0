from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

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
    ("actif", "Actif"),
    ("inactif", "Inactif"),
    ("maintenance", "En maintenance"),
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
    attribut = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    etat = models.CharField(max_length=50, choices=ETAT_CHOICES)
    zone = models.CharField(max_length=50, choices=ZONE_CHOICES)
    annee_achat = models.IntegerField(null=True, blank=True)
    annee_fin = models.IntegerField(null=True, blank=True)
    duree_max_jour = models.IntegerField(null=True, blank=True)
    connectivite = models.CharField(max_length=100)
    couleur = models.CharField(max_length=50, null=True, blank=True)
    derniere_maintenance = models.DateField(null=True, blank=True)
    image = models.URLField(max_length=300, null=True, blank=True)
    inclinaison_max = models.CharField(max_length=50, null=True, blank=True)
    marque = models.CharField(max_length=100)
    puissance = models.CharField(max_length=50, null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif')
    vitesse_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    intensite = models.IntegerField(null=True, blank=True)
    heure_debut_utilisation = models.TimeField(null=True, blank=True)
    heure_fin_utilisation = models.TimeField(null=True, blank=True)
    puissance_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    vitesse_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    intensite_max = models.IntegerField(null=True, blank=True)
    type_transmission = models.CharField(max_length=100, null=True, blank=True)
    type_resistance = models.CharField(max_length=100, null=True, blank=True)
    amorti = models.CharField(max_length=100, null=True, blank=True)
    ventilation_frontale = models.BooleanField(null=True, blank=True)
    hauteur_marche = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    longueur_rail = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    type_mouvement = models.CharField(max_length=100, null=True, blank=True)
    est_disponible = models.BooleanField(default=True)
    calories_brulees = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    duree_utilisation = models.IntegerField(null=True, blank=True)
    longueur_pas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    distance_parcourue = models.FloatField(null=True, blank=True, help_text="Distance parcourue pendant l'utilisation (en km)")


    def __str__(self):
        return f"{self.nom} ({self.get_type_display()})"

class HistoriqueUtilisation(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    objet = models.ForeignKey('ObjetConnecte', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)
    etat = models.CharField(max_length=50, choices=ETAT_CHOICES)
    image = models.URLField(max_length=300, null=True, blank=True)



    # Champs copiés depuis ObjetConnecte
    vitesse_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    puissance = models.CharField(max_length=50, null=True, blank=True)
    inclinaison_max = models.CharField(max_length=50, null=True, blank=True)
    intensite = models.IntegerField(null=True, blank=True)
    amorti = models.CharField(max_length=100, null=True, blank=True)
    ventilation_frontale = models.BooleanField(null=True, blank=True)
    hauteur_marche = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    longueur_rail = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    longueur_pas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    type_transmission = models.CharField(max_length=100, null=True, blank=True)
    type_resistance = models.CharField(max_length=100, null=True, blank=True)
    type_mouvement = models.CharField(max_length=100, null=True, blank=True)
    distance_parcourue = models.FloatField(null=True, blank=True, help_text="Distance parcourue pendant l'utilisation (en km)")



    def __str__(self):
        return f"{self.utilisateur.username} - {self.objet.nom} - {self.action}"



class ObjetSelectionne(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    objet = models.ForeignKey(ObjetConnecte, on_delete=models.CASCADE)
    MUSIQUE_CHOICES = [
        ('aucune', 'Aucune'),
        ('rap', 'Rap'),
        ('classique', 'Classique'),
        ('jazz', 'Jazz'),
        ('pop', 'Pop'),
        ('rock', 'Rock'),
        ('electro', 'Electro'),
        ('reggae', 'Reggae'),
        ('country', 'Country'),
        ('hiphop', 'Hip-hop'),
        ('rnb', 'R&B'),
        ('latino', 'Latino'),
        ('kpop', 'K-Pop'),
    ]

    LUMIERE_CHOICES = [
        ('basse', 'Basse'),
        ('moyenne', 'Moyenne'),
        ('forte', 'Forte'),
    ]

    CLIM_CHOICES = [
        ('on', 'ON'),
        ('off', 'OFF'),
    ]
    
    AMBIANCE_CHOICES = [
        ('aucune', 'Aucune'),
        ('zen', 'Zen'),
        ('cardio', 'Cardio'),
        ('motivation', 'Motivation'),
        ('muscu', 'Musculation'),
    ]
        

    ambiance = models.CharField(max_length=20, choices=AMBIANCE_CHOICES, blank=True, null=True)
    musique = models.CharField(max_length=20, choices=MUSIQUE_CHOICES, blank=True, null=True)
    lumiere = models.CharField(max_length=20, choices=LUMIERE_CHOICES, blank=True, null=True)
    climatisation = models.CharField(max_length=5, choices=CLIM_CHOICES, blank=True, null=True)
    temperature = models.IntegerField(blank=True, null=True)
    date_debut = models.DateTimeField(auto_now_add=True)
    duree_heures = models.PositiveIntegerField(default=1) 
    def temps_restant(self):
        fin = self.date_debut + timedelta(hours=self.duree_heures)
        delta = fin - timezone.now()
        if delta.total_seconds() < 0:
            return timedelta(seconds=0)
        return delta
    @property
    def est_encore_reserve(self):
        fin = self.date_debut + timedelta(hours=self.duree_heures)
        return timezone.now() < fin

    class Meta:
        unique_together = ('utilisateur', 'objet')

    def __str__(self):
        return f"{self.utilisateur.username} - {self.objet.nom}"


class HistoriqueAmbiance(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    ambiance = models.CharField(max_length=20, choices=ObjetSelectionne.AMBIANCE_CHOICES)
    musique = models.CharField(max_length=20, choices=ObjetSelectionne.MUSIQUE_CHOICES)
    lumiere = models.CharField(max_length=20, choices=ObjetSelectionne.LUMIERE_CHOICES)
    climatisation = models.CharField(max_length=5, choices=ObjetSelectionne.CLIM_CHOICES)
    temperature = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.date.strftime('%d/%m/%Y %H:%M')}"
