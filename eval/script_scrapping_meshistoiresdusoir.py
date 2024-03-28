import os
import config
#set your environment variable for SSL certificate
certi_path = config.certify
os.environ['REQUESTS_CA_BUNDLE'] = certi_path
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import requests
import random
import time
import json
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy import create_engine
import psycopg2
from pymongo import MongoClient

mongo_db_port = config.mongo_db_port
user = config.postgres_db_user
password = config.postgres_db_password
db = config.postgres_db_db
port = config.postgres_db_port
host = config.postgres_db_host
mongo_db_host = config.mongo_db_host

def initialize_driver(headers_list, proxy_list):
    options = Options()
    #select a random user-agent from the list
    user_agent = random.choice(headers_list)["User-Agent"]
    options.add_argument(f"user-agent={user_agent}")
    
    #select a random proxy from the list
    proxy = random.choice(proxy_list)
    if proxy:
        options.add_argument(f"--proxy-server={proxy}")
    
    #add some common options
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}

    #initialize Chrome WebDriver with the specified options
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    #set implicit wait of 10sec
    driver.implicitly_wait(10)

    return driver

def MainPage(driver, url):
    driver.get(url)
    time.sleep(3)

def nbHisytoryByPage(driver):
    try:
        liste_histoires = driver.find_element(By.ID, "liste_histoires")
        search_results = driver.find_elements(By.TAG_NAME, "article")
        search_results_count = len(search_results)
        return search_results_count

    except Exception as e:
        print("An error occurred in nbHisytoryByPage:", str(e))
        return 0  # Or handle the exception as needed

def nbHisytoryTot(driver):
    try:
        search_results = driver.find_element(By.CSS_SELECTOR, 'div[class="row align-items-center gy-2 mb-4 pb-1 pb-sm-2 pb-lg-3"]')
        text_nb_hostory_tot = search_results.find_element(By.CSS_SELECTOR, 'h2[class="mb-lg-0"]').text.split('(')[1].split(')')[0]
        return int(text_nb_hostory_tot)

    except Exception as e:
        print("An error occurred in nbHisytoryTot:", str(e))
        return 0  # Or handle the exception as needed

def Click(driver, pos):
    '''Click on the link'''
    try:
        element = driver.find_elements(By.CSS_SELECTOR, 'a[class="btn btn-sm btn-primary mb-1"]')[pos]
        element.click()
        return 1

    except Exception as e:
        print("An error occurred in CLICK:", str(e))
        return 0

def ClickMoreHistory(driver):
    '''Click on the link'''
    try:
        element = driver.find_element(By.ID, "loadmorebtn")
        element.click()
        return 1

    except Exception as e:
        print("An error occurred in ClickMoreHistory:", str(e))
        return 0

def GetDatas(driver, story):
    time.sleep(3)
    try:
        age = driver.find_elements(By.CSS_SELECTOR, 'span[class="badge border border-light text-light fs-sm mb-1"]')[1].text
        title = driver.find_element(By.CSS_SELECTOR, 'h1[class="display-2 mb-4"]').text
        history = driver.find_element(By.CSS_SELECTOR, 'div[class="col-lg-9 col-xl-8"]').find_element(By.CSS_SELECTOR, 'div[class="fs-lg"]').get_attribute("outerHTML")
        lien_type_history = driver.find_element(By.CSS_SELECTOR, 'ol[class="pt-lg-3 pb-lg-4 pb-2 breadcrumb"]').find_elements(By.TAG_NAME, 'li')
        category = lien_type_history[3].find_element(By.TAG_NAME, 'a').text
        genre = lien_type_history[4].find_element(By.TAG_NAME, 'a').text

        # Récupération des questions et des réponses
        question_histoire = []
        try:
            accordion_question = driver.find_element(By.ID, "collapseOne")
            all_questions = accordion_question.find_elements(By.CSS_SELECTOR, 'h3[class="lead"]')
            for i in range(0, len(all_questions)):
                div_responses = accordion_question.find_elements(By.CSS_SELECTOR, 'div[class="card mb-4"]')[i]
                all_responses = div_responses.find_elements(By.CSS_SELECTOR, 'label[class="form-check-label"]')
                correction = driver.find_elements(By.CLASS_NAME, 'text-success')[i]
                tab_response = []
                for a in range(0, len(all_responses)):
                    tab_response.append(all_responses[a].get_attribute("textContent"))
                question_histoire.append({
                    "question" + str(i+1): {
                        "enonce":  accordion_question.find_elements(By.CSS_SELECTOR, 'h3[class="lead"]')[i].get_attribute("textContent"),
                        "responses": tab_response,
                        "correction": correction.get_attribute("id").split('_')[2]
                    }
                })
        except NoSuchElementException:
            print("Element collapseOne n'existe pas. Le quiz sera vide.")

        # Récupération du glossaire
        dictionnaire_glossaire = {}
        try:
            accordion_glossaire = driver.find_element(By.ID, "collapseTwo").find_element(By.TAG_NAME, 'dl')
            mots = accordion_glossaire.find_elements(By.TAG_NAME, 'dt')
            defs = accordion_glossaire.find_elements(By.TAG_NAME, 'dd')
            for i in range(0, len(mots)):
                dictionnaire_glossaire[mots[i].get_attribute("textContent")] = defs[i].get_attribute("textContent")
        except NoSuchElementException:
            print("Element collapseTwo n'existe pas. Le glossaire sera vide.")

        current_story = [age, title, history, category, genre, question_histoire, dictionnaire_glossaire]
        story.append(current_story)

        # Écriture dans le fichier
        with open('history.txt', 'a') as f:
            f.write(str(current_story))
            print(f'Écriture du travail : {driver.current_url}')
            f.write('\n')

        return 1

    except Exception as e:
        print(f"Erreur lors de l'analyse HTML : {e}")

driver = initialize_driver([
    {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Host": "httpbin.org",
        "Sec-Ch-Ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    },
    {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Host": "httpbin.org",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
    },
    {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Host": "httpbin.org",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    },
    {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en;q=0.5",
        "Host": "httpbin.org",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"
    },
    {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Host": "httpbin.org",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15"
    }
], [False])

MainPage(driver, r"https://www.meshistoiresdusoir.fr/g/histoires-fantastiques/")

nbHisytoryTotVar = nbHisytoryTot(driver)

nbHisytoryByPageVar = nbHisytoryByPage(driver)

nb_page = nbHisytoryTotVar // nbHisytoryByPageVar
if nbHisytoryTotVar % nbHisytoryByPageVar != 0:
    nb_page = nb_page + 1

story = []
nb_history_page_init = nbHisytoryByPage(driver)
for a in range(0, nb_page):
    nb_history_page = nbHisytoryByPage(driver)
    for i in range((a * nb_history_page_init), nb_history_page):
        Click(driver, i)
        GetDatas(driver, story)
        driver.back()
    time.sleep(3)
    ClickMoreHistory(driver)
    time.sleep(3)

df = pd.DataFrame(story)
df.columns = ["Age", "Titre", "Histoire", "Category", "Genre", "Questions", "Glossaire"]
df = df.sort_values(by=['Age', 'Category', 'Genre'], ascending=[False, False, False])

# Create the connection
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

df['Glossaire'] = df['Glossaire'].apply(json.dumps)
df['Questions'] = df['Questions'].apply(json.dumps)

df.to_sql('story_table', engine, if_exists='replace', index=False)

#connect to the MongoDB server (default is localhost on port 27017)
client = MongoClient(mongo_db_host, mongo_db_port)

#access the database (create it if it doesn't exist)
db = client['story_database']

#access the collection (similar to a table in relational databases)
collection = db['story_collection']

#convert DataFrame to dictionary format and insert into our MongoDB database
collection.insert_many(df.to_dict('records'))

driver.quit()