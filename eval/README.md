# Contexte

    Eval de scrapping sur le site : https://www.meshistoiresdusoir.fr/g/histoires-fantastiques/
    Objectif : 
        - Récupérer les données (le script prend environ 34 minutes pour récuperer toutees les données)
        - Analyser les données
        - Rentrer les données dans une base postgres et mongo

## Modifier le fichier config.py

    Modifier le fichier config.py pour avoir les bonnes connections a la base de données postgres et mongodb
    si docker compose :
        - postgres_db_host = 'postgres' 
        - mongo_db_host = 'mongo'

## Installation sans docker compose

1 **Prérequis :**

   - python et docker

2 **Lancer les images des bases de données :**

    Assurer vous de lancer votre démon docker puis lancer les images suivantes :

   ```
   docker run -d --name mongo_story_db -p 27017:27017 mongo
   ```
   ```
   docker run --name postgres_story_db -d -p 5432:5432 -e POSTGRES_PASSWORD=story_pass postgres:alpine
   ```

3 **Installer les dépendances :**

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