########################################################
#################### IMPORT ############################
########################################################
from random import randint
import bs4
from selenium import webdriver
from time import sleep
import re
import pandas as pd

# Ersetzungen definieren
substitutions = {"1-30": "", "von": " ", "Ergebnissen": "", "\n": "", "\t": ""}

def replace(string, substitutions):
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)

###################################################
#################### ARGUMENTS ####################
###################################################
print ('Und ab geht die Lutzi...')

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    'referer': 'https://www.google.de/'}

# BERUFENET-A-ZListe einlesen
# Buchstabe = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
Buchstabe = 'I'
AZListe = pd.read_csv('Output\\BERUFENET_Buchstabe_' + Buchstabe + '.csv', sep=";", encoding = 'latin-1')

# Bearbeite URL´s für die Unterseiten
elementMods = []
for element in AZListe.itertuples():
    if "Duale Ausbildung" == element[7]:
        elementMod = element[5].replace('&dkz', '/ausbildungsinhalte&dkz')
        elementMods.append(elementMod)

    elif "Studienfach" == element[7]:
        elementMod = element[5].replace('&dkz', '/studieninhalte&dkz')
        elementMods.append(elementMod)

    else:
        elementMods.append(element[5])

elementMods = pd.DataFrame(elementMods)
AZListe['URL_Inhalte'] = elementMods

AZListeFiltered = AZListe.query('`Berufskundliche Gruppe` == "Duale Ausbildung" or `Berufskundliche Gruppe` == "Studienfach"')
AZListeFiltered = AZListeFiltered.loc[~AZListeFiltered["URL_Inhalte"].duplicated(keep='first')]

# Webbrowser starten
driver = webdriver.Chrome("C:\\Users\\BenediktRunschkeWifO\\\OneDrive - WifOR\\Desktop\\chromedriver.exe")

mxAusbildungAll = pd.DataFrame(columns=["Kurze_Berufsbezeichnung", "Inhalte"])
mxStudiumAll = pd.DataFrame(columns=["Kurze_Berufsbezeichnung", "Inhalte"])
mxRestAll = pd.DataFrame(columns=["Kurze_Berufsbezeichnung", "Inhalte"])
mxAll = pd.DataFrame(columns=["Kurze_Berufsbezeichnung", "Inhalte"])

for item in AZListeFiltered.itertuples():
    driver.get(item[8])
    sleep(randint(2,10))
    Html = driver.page_source
    Soup = bs4.BeautifulSoup(Html, 'lxml')

    beruf = item[6]

    betrieb_inhalte = []
    schule_inhalte = []
    zusatz_inhalte = []
    ausbildung_inhalte = []
    studium_inhalte1 = []
    studium_inhalte2 = []
    studium_inhalte3 = []
    studium_inhalte4 = []
    studium_inhalte5 = []

    ###Ausbildungsinhalte
    if "Duale Ausbildung" == item[7]:
        # Ausbildungsbetrieb
        inhalt = Soup.findAll(id="a11-0_1_Content_1")
        try:
            inhalt = inhalt[0].contents
            for k in range(1, len(inhalt), 2):
                ausbildung = inhalt[k].text
                ausbildung = replace(ausbildung, substitutions).strip()
                betrieb_inhalte.append(ausbildung)
        except IndexError:
            pass

        #Berufsschule
        inhalt = Soup.findAll(id="a11-0_2_Content_2")
        try:
            inhalt = inhalt[0].contents
            for k in range(1, len(inhalt), 2):
                ausbildung = inhalt[k].text
                ausbildung = replace(ausbildung, substitutions).strip()
                schule_inhalte.append(ausbildung)
        except IndexError:
            pass

        # Zusatzqualifikationen
        inhalt = Soup.findAll(id="a10-3_0_Content_1")
        try:
            inhalt = inhalt[0].contents
            for k in range(1, len(inhalt), 2):
                ausbildung = inhalt[k].text
                ausbildung = replace(ausbildung, substitutions).strip()
                zusatz_inhalte.append(ausbildung)
        except IndexError:
            pass

        # Zusammenfügen
        ausbildung_inhalte.extend(betrieb_inhalte)
        ausbildung_inhalte.extend(schule_inhalte)
        ausbildung_inhalte.extend(zusatz_inhalte)

        ausbildung_inhalte = pd.Series(ausbildung_inhalte)
        berufe = pd.Series([beruf] * len(ausbildung_inhalte))

        mxAusbildung = pd.concat([berufe, ausbildung_inhalte], axis=1)
        mxAusbildung = mxAusbildung.rename(columns={mxAusbildung.columns[0]: "Kurze_Berufsbezeichnung", mxAusbildung.columns[1]: "Inhalte"})
        mxAusbildungAll = mxAusbildungAll.append(mxAusbildung)
        print('Ausbildungsinhalte vom Beruf ' + item[6] + ' wurden abgezogen. Check.')

    ###Studieninhalte
    elif "Studienfach" == item[7]:

        # Studieninhalte 1
        inhalt = Soup.findAll(id="a11-0_1_Content_1")
        try:
            inhalt = inhalt[0].contents

            for k in range(1, len(inhalt), 2):
                studium = inhalt[k].text
                studium = replace(studium, substitutions).strip()
                studium_inhalte1.append(studium)
        except IndexError:
            pass

        # Studieninhalte 2
        inhalt = Soup.findAll(id="a11-0_2_Content_2")
        try:
            inhalt = inhalt[0].contents

            for k in range(1, len(inhalt), 2):
                studium = inhalt[k].text
                studium = replace(studium, substitutions).strip()
                studium_inhalte2.append(studium)
        except IndexError:
            pass

        # Studieninhalte 3
        inhalt = Soup.findAll(id="a11-0_3_Content_3")
        try:
            inhalt = inhalt[0].contents

            for k in range(1, len(inhalt), 2):
                studium = inhalt[k].text
                studium = replace(studium, substitutions).strip()
                studium_inhalte3.append(studium)
        except IndexError:
            pass

        # Studieninhalte 4
        inhalt = Soup.findAll(id="a11-0_4_Content_4")
        try:
            inhalt = inhalt[0].contents

            for k in range(1, len(inhalt), 2):
                studium = inhalt[k].text
                studium = replace(studium, substitutions).strip()
                studium_inhalte4.append(studium)
        except IndexError:
            pass

        # Studieninhalte 5
        inhalt = Soup.findAll(id="a11-0_5_Content_5")
        try:
            inhalt = inhalt[0].contents

            for k in range(1, len(inhalt), 2):
                studium = inhalt[k].text
                studium = replace(studium, substitutions).strip()
                studium_inhalte5.append(studium)
        except IndexError:
            pass

        # Zusammenfügen
        studium_inhalte1.extend(studium_inhalte2)
        studium_inhalte1.extend(studium_inhalte3)
        studium_inhalte1.extend(studium_inhalte4)
        studium_inhalte1.extend(studium_inhalte5)

        studium_inhalte1 = pd.Series(studium_inhalte1)
        berufe = pd.Series([beruf] * len(studium_inhalte1))

        mxStudium = pd.concat([berufe, studium_inhalte1], axis=1)
        mxStudium = mxStudium.rename(columns={mxStudium.columns[0]: "Kurze_Berufsbezeichnung", mxStudium.columns[1]: "Inhalte"})
        mxStudiumAll = mxStudiumAll.append(mxStudium)

        print('Studieninhalte vom Beruf ' + item[6] + ' wurden abgezogen. Check.')

    else:
        ausbildung = 'NA'
        betrieb_inhalte.append(ausbildung)
        betrieb_inhalte = pd.Series([betrieb_inhalte])
        berufe = pd.Series([beruf])

        mxRest = pd.concat([berufe, betrieb_inhalte], axis=1)
        mxRest = mxRest.rename(columns={mxRest.columns[0]: "Kurze_Berufsbezeichnung", mxRest.columns[1]: "Inhalte"})
        mxRestAll = mxRestAll.append(mxRest)
        print('Filter hat nicht funktioniert. Selbstzerstörungsmodus in 3, 2, 1.... Puffff.')

mxAll = mxAll.append(mxAusbildungAll).append(mxStudiumAll).append(mxRestAll)
mxAllOutput = pd.merge(mxAll, AZListeFiltered, on = ["Kurze_Berufsbezeichnung"], sort = False)
mxAllOutput.to_csv('Output\\Ausbildungs-Studieninhalte_Buchstabe_' + Buchstabe + '.csv', sep=";", encoding="utf8")
