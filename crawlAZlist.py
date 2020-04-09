########################################################
#################### IMPORT ############################
########################################################
import bs4
from selenium import webdriver
from time import sleep
from random import randint
import re
import math
import pandas as pd
# Ersetzungen definieren
substitutions = {"1-30": "", "von": " ", "Ergebnissen": "", "Systematiknummer: ": "", "Berufs-ID: ": "",
                 "Studienfach: ": "", "Ausbildung: ": "", "Tätigkeit: ": "", " Ergebnis": "", " Ergebnisse": "", "31-36\xa0 \xa036": "36"}

def replace(string, substitutions):
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)

# Hilfslisten definieren
# abc = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
abc = ["J"]

###################################################
#################### ARGUMENTS ####################
###################################################
print('Schon wieder ne Aufgabe für mich?' + '\n' + 'Na gut, ich crawl mal nach: ')
BasisUrl = 'https://berufenet.arbeitsagentur.de/berufenet/faces/index?path=null/sucheAZ&let=A'

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/74.0',
    'referer': 'https://www.google.de/'}


# Webbrowser starten
driver = webdriver.Chrome("C:\\Users\\BenediktRunschkeWifO\\\OneDrive - WifOR\\Desktop\\chromedriver.exe")
occupations = []
fields = []
for j in abc:
    Url = 'https://berufenet.arbeitsagentur.de/berufenet/faces/index?path=null/sucheAZ&let=' + j
    driver.get(Url)
    sleep(randint(2,10))
    Html = driver.page_source
    Soup = bs4.BeautifulSoup(Html, 'lxml')
    # Gesamtanzahl der Einträge
    NoOfEntries = Soup.findAll(class_="bapf-accessible-table-filter-ergebnisse")
    NoOfEntries = NoOfEntries[0].string
    NoOfEntries = replace(NoOfEntries, substitutions).strip()
    noOfPages = int(math.ceil(int(NoOfEntries) / 30))
    # Durchlaufe Unterseiten
    for _ in range(noOfPages):
        Html = driver.page_source
        Soup = bs4.BeautifulSoup(Html, 'lxml')
        beruf = Soup.findAll(class_="bapf-accessible-table-layout selectable")
        beruf = beruf[0].contents[0].contents
        # Extrahiere Berufe und Berufsfelder
        for i in beruf:
            occupation = i.contents[0].text
            replace(occupation, substitutions)
            field = i.contents[1].text
            replace(field, substitutions)
            occupations.append(occupation)
            fields.append(field)
        try:
            driver.find_element_by_xpath("//*[@id='pt1:r1:0:pt1:tbl_suche_az:dc_cl4']").click()
        except:
            pass
        sleep(randint(2,10))
datazip = list(zip(occupations, fields))
mxBerufsliste = pd.DataFrame(datazip, columns=["Kurze_Berufsbezeichnung", "Berufskundliche Gruppe"])
print('Berufsliste ist vollständig geladen.')


###################################################
################# Einzelseiten ####################
###################################################
currentURLs = []
occupations2 = []
dkzs = []
sysNos = []
mxAll = pd.DataFrame(columns=["Berufsbezeichnung", "Berufs-ID", "Systematiknummer", "URL"])
for j in abc:
    # Anpassung
    mxAll_temp = []
    Url = 'https://berufenet.arbeitsagentur.de/berufenet/faces/index?path=null/sucheAZ&let=' + j
    driver.get(Url)
    sleep(randint(2,10))

    # Rufe jeweils die aktuelle Suppe der Seite auf
    Html = driver.page_source
    Soup = bs4.BeautifulSoup(Html, 'lxml')

    # Bestimme Gesamtanzahl der Berufe je Buchstaben
    NoOfEntries = Soup.findAll(class_="bapf-accessible-table-filter-ergebnisse")
    NoOfEntries = NoOfEntries[0].string
    NoOfEntries = replace(NoOfEntries, substitutions).strip()

    # Berechne Anzahl der Berufe auf letzter Seite
    NoOccupLastSite = float(NoOfEntries) / 30
    NoOccupLastSite = str(NoOccupLastSite)
    NoOccupLastSite = float('0.' + NoOccupLastSite.split(".")[1])*30
    NoOccupLastSite = int(NoOccupLastSite)

    # Berechne Anzahl an Unterseiten je Buchstabe
    noOfPages = int(math.ceil(int(NoOfEntries) / 30))

    # Clicke auf Berufsseite und ziehe URL
    for k in range(noOfPages):  # k zählt den aktuellen Beruf 'noOfPages'
        # Prüfung ob auf letzter Seite
        if k == noOfPages - 1:
            AnzahlBerufe = NoOccupLastSite
        else:
            AnzahlBerufe = 30

        for l in range(AnzahlBerufe):  # l läuft über die 30 Einzelelemente jeder Seite

            print('Starte jetzt mit Beruf ' + str(l+1))

            driver.get(Url)
            sleep(randint(2,10))
            print('Schritt 1 abgeschlossen')

            # Bestimme auf welcher Unterseite er sich gerade befindet und klicke wieder an die richtige Stelle
            site_indicator = int(k)
            for seite in range(int(site_indicator)):
                driver.find_element_by_xpath("//*[@id='pt1:r1:0:pt1:tbl_suche_az:dc_cl4']").click()
                sleep(randint(2,10))
            print('Schritt 2 abgeschlossen: Chill gerade auf Seite ' + str(k + 1))

            xpath = "//*[@id='pt1:r1:0:pt1:tbl_suche_az:i1:" + str(l) + ":cf9']"

            startseite = False
            while not startseite:
                try:
                    driver.find_element_by_xpath(xpath).click()
                    sleep(randint(10,15))
                    currentURL = driver.current_url

                    if currentURL == Url:
                        startseite = False
                        print('Nope, das hat nicht geklappt.')
                    else:
                        startseite = True
                        print('Yes! Commander wir haben das Ziel erreicht.')
                except:
                    pass
            print('Schritt 3 abgeschlossen')

            # Das Element der Systematikinformationen ist manchmal nicht verfügbar. Schleife führt dazu, dass er so lange probiert bis es geht.
            connected = False
            while not connected:
                try:
                    # Öffne Systematikinformationen
                    driver.find_element_by_class_name("af_panelAccordion_header-title").click()
                    sleep(randint(2,10))
                    connected = True
                except:
                    pass
            print('Schritt 4 abgeschlossen')

            sleep(3)
            sysInfo = driver.find_element_by_class_name("af_showDetailItem").text
            sysInfo = pd.Series(sysInfo)
            sysInfo = sysInfo.str.split("\n", expand=True)
            sysInfo = sysInfo.transpose()

            sysInfo_subsetOcc = sysInfo[sysInfo[0].str.contains('Tätigkeit:|Ausbildung:|Studienfach:')]
            sysInfo_subsetDkz = sysInfo[sysInfo[0].str.contains('Berufs-ID:')]
            sysInfo_subsetSys = sysInfo[sysInfo[0].str.contains('Systematiknummer:')]

            currentURL = pd.Series([currentURL] * len(sysInfo_subsetOcc))
            currentURL = pd.DataFrame(currentURL)

            sysInfo_subsetOcc = sysInfo_subsetOcc.rename(columns={sysInfo_subsetOcc.columns[0]: "Berufsbezeichnung"})
            sysInfo_subsetOcc2 = sysInfo_subsetOcc
            sysInfo_subsetOcc2 = sysInfo_subsetOcc2.rename(columns={sysInfo_subsetOcc2.columns[0]: "Kurze_Berufsbezeichnung"})
            sysInfo_subsetDkz = sysInfo_subsetDkz.rename(columns={sysInfo_subsetDkz.columns[0]: "Berufs-ID"})
            sysInfo_subsetSys = sysInfo_subsetSys.rename(columns={sysInfo_subsetSys.columns[0]: "Systematiknummer"})
            currentURL = currentURL.rename(columns={currentURL.columns[0]: "URL"})

            sysInfo_subsetOcc2['Kurze_Berufsbezeichnung'] = sysInfo_subsetOcc2['Kurze_Berufsbezeichnung'].str.replace(r'Tätigkeit: ', '').str.replace(r'Ausbildung: ', '').str.replace(r'Studienfach: ', '')
            sysInfo_subsetDkz['Berufs-ID'] = sysInfo_subsetDkz['Berufs-ID'].str.replace(r'Berufs-ID: ', '')
            sysInfo_subsetSys['Systematiknummer'] = sysInfo_subsetSys['Systematiknummer'].str.replace(r'Systematiknummer: ', '')

            mxOccupAll = pd.concat([sysInfo_subsetOcc2.reset_index(drop=True), sysInfo_subsetOcc.reset_index(drop=True), sysInfo_subsetDkz.reset_index(drop=True),
                                    sysInfo_subsetSys.reset_index(drop=True), currentURL], axis=1)
            mxAll = mxAll.append(mxOccupAll)

            print('Beruf ' + str(l + 1) + ' von 30 auf dieser Seite hab ich schon abgearbeitet. Ich bin ganz schön fleißig.....')
        sleep(randint(2,10))

    # Anpassung
    mxAll_temp = pd.merge(mxAll, mxBerufsliste, on=["Kurze_Berufsbezeichnung"], sort=False)
    mxAll_temp.to_csv('Output\\BERUFENET_Buchstabe_' + j +'.csv', sep=";")
    print('Bin mit Buchstabe ' + j + ' fertig und mache jetzt mit dem nächsten weiter. Sklaventreiber du bist....')

# CSV File schreiben
mxAll = pd.merge(mxAll, mxBerufsliste, on = ["Kurze_Berufsbezeichnung"], sort = False)
mxAll.to_csv('Output\\BERUFENET_A-Z_Liste.csv', sep=";")