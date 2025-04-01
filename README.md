# 🏋️ Salle de Sport 2.0

Bienvenue dans **Salle de Sport 2.0**, une plateforme web intelligente développée avec **Django** et **Supabase**.  
Elle permet à une salle de sport d’offrir une **expérience connectée** à ses utilisateurs via des objets intelligents.

---

## 🚀 Fonctionnalités principales

- Authentification des utilisateurs (inscription / connexion / déconnexion)
- Gestion des profils avec sexe, date de naissance, niveau d'expérience
- Page d'accueil dynamique selon l’état de connexion
- Affichage personnalisé : "Bienvenue Moussa" si connecté
- Objets connectés centralisés (tapis, balance, lumière, etc.)
- Historique des interactions utilisateurs ↔ équipements
- Interface admin Django complète

---

## 🔧 Technologies utilisées

- ⚙️ **Backend** : Django 5.x
- 🧠 **Base de données** : Supabase (PostgreSQL)
- 🎨 **Frontend** : HTML + CSS (avec images statiques)
- 🔐 **Authentification** : Django + gestion de profil étendu
- ☁️ **Déploiement possible** : Railway, Render, ou VPS personnel

---

## 📦 Installation locale

1. Cloner le dépôt :

```bash
git clone https://github.com/Charx19/Salle-de-Sport-2.0.git
cd Salle-de-Sport-2.0

 ##🔒 2. Créer un environnement virtuel 
 python -m venv env
env\Scripts\activate          # (Windows)
# ou
source env/bin/activate       # (Mac/Linux)


## 📦 3. Installer les dépendances
pip install -r requirements.txt

 ## Lancer le serveur local
 python manage.py runserver




