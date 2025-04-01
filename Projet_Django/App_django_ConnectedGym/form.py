from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ProfilUtilisateur

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Prénom'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Nom'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    sexe = forms.ChoiceField(choices=[('Homme', 'Homme'), ('Femme', 'Femme')], required=False)
    date_naissance = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    niveau_experience = forms.ChoiceField(
        choices=[
            ('débutant', 'Débutant'),
            ('intermédiaire', 'Intermédiaire'),
            ('avancé', 'Avancé'),
            ('expert', 'Expert')
        ],
        initial='débutant',
        required=True
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            ProfilUtilisateur.objects.create(
                user=user,
                sexe=self.cleaned_data.get('sexe'),
                date_naissance=self.cleaned_data.get('date_naissance'),
                niveau_experience=self.cleaned_data.get('niveau_experience')
            )
        return user
