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




🔧 GUIDE COMPLET GIT + GITHUB (VS CODE) — MOUSSA 💻

===========================================
1. ✅ OUVRIR TON PROJET VS CODE
===========================================
cd "C:\Users\mouss\OneDrive\Bureau\GITHUB\Salle-de-Sport-2.0"
code .

===========================================
2. ✅ VÉRIFIER L'ÉTAT DE TON CODE
===========================================
git status

===========================================
3. ✅ AJOUTER LES FICHIERS MODIFIÉS
===========================================
➕ Tous les fichiers :
git add .

➕ Fichier spécifique :
git add chemin/fichier.py

===========================================
4. ✅ ENREGISTRER (COMMIT)
===========================================
git commit -m "Message clair ici"

Exemple :
git commit -m "Mise à jour de profil.html"

===========================================
5. ✅ ENVOYER VERS GITHUB (PUSH)
===========================================
git push origin main

(si tu travailles dans une autre branche)
git push origin dev

===========================================
6. ✅ VOIR LES BRANCHES EXISTANTES
===========================================
git branch -a

===========================================
7. ✅ SE PLACER SUR UNE AUTRE BRANCHE
===========================================
git checkout nom-de-la-branche

Exemple :
git checkout dev

===========================================
8. ✅ CRÉER UNE NOUVELLE BRANCHE
===========================================
git checkout -b nouvelle-branche

Exemple :
git checkout -b ajout-accueil-responsive

===========================================
9. ✅ FUSIONNER UNE BRANCHE DANS MAIN
===========================================
git checkout main
git pull origin main
git merge nom-de-la-branche
git push origin main

===========================================
10. 🔁 RÉSOUDRE CONFLIT SI NÉCESSAIRE
===========================================
1. Ouvrir le fichier en conflit
2. Choisir la bonne version
3. Supprimer les lignes <<<<<<< / ======= / >>>>>>>
4. Ensuite :
   git add .
   git rebase --continue
   git push origin main




