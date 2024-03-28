# Contexte

    Eval de scraping sur le site : https://www.meshistoiresdusoir.fr/g/histoires-fantastiques/
    Objectif : 
        - récupérer les données
        - Analyser les données
        - Rentrer les données dans une base postgres et mongo

## Modifier le fichier config.py

    Modifier le fichier config.py pour avoir les bonnes connexions à la base de données postgres et mongodb
    si docker compose :
        - postgres_db_host = 'postgres' 
        - mongo_db_host = 'mongo'

## Installation sans docker compose

1 **Prérequis :**

   - python et docker

2 **Lancer les images des bases de données :**

   Assurer-vous de lancer votre démon docker puis lancer les images suivantes :

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
   python script_scrapping_meshistoiresdusoir.py
   ```

## Explication de code

1 **Docker compose :**

   J'ai fait un docker compose avec une image de postgres, mongo normale
   Mais j'ai build une image python à partir d'un Dockerfile afin de pouvoir installer lors de la création de l'image Chrome, chrome_driver et les imports du requirements.txt

![alt text](https://github.com/bertreux/M1_PYTHON-_WEBSCRAPPING/blob/main/eval/doc/image/dockerfile.png?raw=true)

2 **Option du web driver :**

![alt text](https://github.com/bertreux/M1_PYTHON-_WEBSCRAPPING/blob/main/eval/doc/image/option_web_driver.png?raw=true)

   Pour les options du web driver j'ai choisi de mettre le --headless, --no-sandbox et --disable-dev-shm-usage parce que lors de l'utilisation de selenium dans un container, chrome ne marchait pas sans

3 **Loop :**

![alt text](https://github.com/bertreux/M1_PYTHON-_WEBSCRAPPING/blob/main/eval/doc/image/loop.png?raw=true)

   Cette boucle au départ ne marchait qu'en mode non headless parce que j'utilisais driver back() qui gardait le fait d'avoir cliqué sur le bouton précédemment
   J'ai donc dû la modifier pour pouvoir cliquer pour chaque histoire le nombre de fois qu'il faut sur le bouton qui charge plus d'histoires

4 **Fonction ClickMoreHistory :**

![alt text](https://github.com/bertreux/M1_PYTHON-_WEBSCRAPPING/blob/main/eval/doc/image/fonction_click_more_history.png?raw=true)

   Cette fonction au départ ne marchait qu'en mode non headless, en mode headless j'avais une erreur pour me dire qu'un element div.container était devant l'élément. J'ai donc modifié le code afin d'abord d'attendre que l'élément soit bien cliquable (jusqu'à 10s) puis je scroll jusqu'au bouton, je le clique et j'attends 3 secondes pour etre sur d'avoir bien toutes les histoires qui sont apparus

5 **Fonction GetDatas :**

   Cette fonction est la fonction qui va récupérer toutes les informations de la page après avoir cliquer sur l'histoire :

![alt text](https://github.com/bertreux/M1_PYTHON-_WEBSCRAPPING/blob/main/eval/doc/image/get_datas_part_1.png?raw=true)

   - Tout d'abors on va attendre 3 secondes pour etre sur que tous les éléments sont bien apparus sur la page
   - Puis on va chercher les éléments les plus simples de la page :
      - age, title, history, category, genre

![alt text](https://github.com/bertreux/M1_PYTHON-_WEBSCRAPPING/blob/main/eval/doc/image/get_datas_part_2.png?raw=true)

   - Puis on va chercher les questions de l'histoire :
      - Je fais cette partie dans un try car il se peut que l'histoire ne possède pas de question et donc si il n'y en, me retourne une erreur. Ainsi si il y a une erreur je dis que question vaut un array vide 
      - Si il y a des questions alors je vais chercher l'élément qui possède toutes les questions. Je vais boucler sur toutes les questions et pour chaque question je vais chercher les réponses et la correction. Après je créais un dictionnaire avec toutes les valeurs et je rentre ce dictionnaire dans un array

![alt text](https://github.com/bertreux/M1_PYTHON-_WEBSCRAPPING/blob/main/eval/doc/image/get_datas_part_3.png?raw=true)

   - Après je récupère le glossaire de l'histoire :
      - Pareille que pour les questions je le fais dans un try catch car il se peut qu'il n'y ait pas de glossaire
      - Si il y a un glossaire alors je vais chercher l'élement qui possède tout le glossaire. Et on trouve que pour chaque mot du glossaire on a une balise dt pour le mot et une balise dd pour la définition. Je boucle donc sur ces deux éléments afin de créer un dictionnaire avec tous le glossaire
   - Je crée après un array avec toutes les valeurs trouvés, l'ajoute au tableau de toutes les histoires et remplis un fichier history.txt avec les valeurs