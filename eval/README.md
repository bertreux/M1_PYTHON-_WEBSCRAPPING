# Contexte

    Eval de scrapping sur le site : https://www.meshistoiresdusoir.fr/g/histoires-fantastiques/
    Objectif : 
        - Récupérer les données (le script prend environ 34 minutes pour récuperer toutees les données)
        - Analyser les données
        - Rentrer les données dans une base postgres et mongo

## Modifier le fichier config.py

    Modifier le fichier config.py pour avoir les bonnes connections a la base de données postgres et mongodb
    si docker compose :
        - postgres_db_host = 'localhost' 
        - mongo_db_host = 'localhost'

## Installation sans docker compose

1 **Prérequis :**

   - python et docker


2 **Installer les dépendances :**

   ```
   pip install --no-cache-dir -r requirements.txt
   ```

# Guide d'utilisation

   Pour utiliser le script veuillez lancer votre démon docker puis lancer le fichier script_scrapping_meshistoiresdusoir.py

   ```
   py script_scrapping_meshistoiresdusoir.py
   ```

## Docker compose

1**Lancer les images :**

   ```
   docker compose up -d
   ```

2**Lancer le script :**

   ```
   docker compose exec -ti python bash
   ```

   Lancer le fichier script_scrapping_meshistoiresdusoir.py

   ```
   py script_scrapping_meshistoiresdusoir.py
   ```