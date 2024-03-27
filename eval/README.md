# Contexte

    Eval de scrapping sur le site : https://www.meshistoiresdusoir.fr/g/histoires-fantastiques/
    Objectif : 
        - Récupérer les données (le script prend environ 34 minutes pour récuperer toutees les données)
        - Analyser les données
        - Rentrer les données dans une base postgres et mongo

## Installation sans docker compose

1 **Prérequis :**

   - python et docker


2 **Installer les dépendances :**

   ```
   pip install 
   ```

# Guide d'utilisation

   Pour utiliser le script veuillez lancer votre démon docker puis de lancer intégralement le fichier selenium_scrapping_meshistoiresdusoir.ipynb

## Docker compose

1**Lancer les images :**

   ```
   docker compose up -d
   ```

2**Lancer le script :**

   ```
   docker compose exec -ti python bash
   ```

   Lancer intégralement le fichier selenium_scrapping_meshistoiresdusoir_compose.ipynb