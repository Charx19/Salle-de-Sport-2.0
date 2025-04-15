from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import ProfilUtilisateur

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    sexe = forms.ChoiceField(choices=[('Homme', 'Homme'), ('Femme', 'Femme')], required=False)
    date_naissance = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

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
                niveau_experience='débutant'
            )
        return user

class ProfilUtilisateurForm(forms.ModelForm):
    first_name = forms.CharField(label='Prénom', max_length=30)
    last_name = forms.CharField(label='Nom', max_length=30)
    email = forms.EmailField(label='Email')

    class Meta:
        model = ProfilUtilisateur
        fields = ['sexe', 'date_naissance', 'photo_profil']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email

    def save(self, commit=True):
        profil = super().save(commit=False)
        user = profil.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profil.save()
        return profil
