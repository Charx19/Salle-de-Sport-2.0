from django.db import models
from django.contrib.auth.models import User

class ProfilUtilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sexe = models.CharField(max_length=10, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    niveau_experience = models.CharField(max_length=50, default='débutant')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class ObjetConnecte(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    etat = models.CharField(max_length=50)
    attributs = models.JSONField()

    def __str__(self):
        return self.nom

class HistoriqueUtilisation(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    objet = models.ForeignKey(ObjetConnecte, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.objet.nom} - {self.action}"
