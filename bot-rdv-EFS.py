
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Python 3.9
from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
from selenium import webdriver
import time
import os

date_lundi = "18-07-2022" # date JJ-MM-AAAA du lundi de la semaine recherchée : ex: 18-07-2022
jour = "samedi" # jour de la semaine pour lequel un créneau est recheché ; ex: samedi

semainiers = {
"Trinité plasma" : "https://mon-rdv-dondesang.efs.sante.fr/collecte/2888/plasma/" + date_lundi,
"Crozatier plasma" : "https://mon-rdv-dondesang.efs.sante.fr/collecte/2897/plasma/"  + date_lundi,
"Bichat plasma" : "https://mon-rdv-dondesang.efs.sante.fr/collecte/2900/plasma/" + date_lundi,
"Saint-Louis plasma" : "https://mon-rdv-dondesang.efs.sante.fr/collecte/2896/plasma/" + date_lundi,
"Pompidou plasma" : "https://mon-rdv-dondesang.efs.sante.fr/collecte/2899/plasma/" + date_lundi,
"Pitié Salpétrière plasma" : "https://mon-rdv-dondesang.efs.sante.fr/collecte/3042/plasma/" + date_lundi,
"Trinité plaquettes" : "https://mon-rdv-dondesang.efs.sante.fr/collecte/2888/plaquettes/" + date_lundi,
"Crozatier plaquettes" : "https://mon-rdv-dondesang.efs.sante.fr/collecte/2897/plaquettes/" + date_lundi,
"Bichat plaquettes" : "https://mon-rdv-dondesang.efs.sante.fr/collecte/2900/plaquettes/" + date_lundi,
"Saint-Louis plaquettes" : "https://mon-rdv-dondesang.efs.sante.fr/collecte/2896/plaquettes/" + date_lundi,
"Pompidou plaquettes" : "https://mon-rdv-dondesang.efs.sante.fr/collecte/2899/plaquettes/" + date_lundi,
"Pitié Salpétrière plaquettes" : "https://mon-rdv-dondesang.efs.sante.fr/collecte/3042/plaquettes/" + date_lundi
}

browser = webdriver.Chrome('./chromedriver')

print("TEST SON...")
# SoX must be installed using 'sudo apt-get install sox' in the terminal
os.system('play -n synth 1 sin 440')
os.system('play -n synth 0.1 sin 400')
os.system('play -n synth 0.1 sin 420')

def alerte(semainier,url):
    while True:
        os.system('play -n synth 0.3 sin 440')
        os.system('play -n synth 0.1 sin 400')
        os.system('play -n synth 0.1 sin 420')
        print("CRENEAU DISPONIBLE :",semainier, "-", url)
        time.sleep(20)

def main():
    compteur_semainier = 0
    creneau_dispo = False
    while creneau_dispo == False:
        semainier = list(semainiers.keys())[compteur_semainier]
        url = list(semainiers.values())[compteur_semainier]
        print(datetime.now(), "-", semainier, "-", url, ": ", end = '')
        response = requests.get(url)
        if response.status_code != 200: print("Réponse site EFS : " + str(response.status_code))
        if response.status_code == 200:
            html = response.content
            browser.get(url)
            time.sleep(10)
            soup = bs(browser.page_source, "html.parser")
            semaine = soup.find(class_="semainier-row semainier-row-day")
            lignes = str(semaine).splitlines()
            for ligne in lignes:
                if ligne.find(jour) != -1:
                    if ligne.find("""<div class="semainier-col semainier-day-title">""") != -1:
                        print(" ")
                        creneau_dispo = True
                        alerte(semainier,url)
                    if ligne.find("""<div class="semainier-col semainier-day-title is-empty">""") != -1: print("pas de dispo", end = '')
            print(" ")
        if compteur_semainier == len(semainiers)-1:
            print("")
            compteur_semainier = 0
        else:
            compteur_semainier += 1
        time.sleep(60)

if __name__ == "__main__":
    main()
