########################################################
#################### IMPORT ############################
########################################################
import pandas as pd

AZListe = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","Y","Z"]

ListeAll = pd.DataFrame(columns=["Kurze_Berufsbezeichnung", "Inhalte", "Berufsbezeichnung", "Berufs-ID", "Systematiknummer", "URL", "Berufskundliche Gruppe", "URL_Inhalte"])
for letter in AZListe:
    Liste = pd.read_csv('Output\\Ausbildungs-Studieninhalte_Buchstabe_' + letter + '.csv', sep=";", encoding = 'latin-1')
    ListeAll = pd.concat([ListeAll, Liste], axis=0)

ListeAll.to_csv('Output\\Ausbildungs-Studieninhalte_A-Z.csv', sep=";", encoding = 'latin-1')



ListeAll = pd.DataFrame(columns=["Berufsbezeichnung", "Kurze_Berufsbezeichnung", "Berufs-ID", "Systematiknummer", "URL", "Berufskundliche Gruppe"])
for letter in AZListe:
    Liste = pd.read_csv('Output\\BERUFENET_Buchstabe_' + letter + '.csv', sep=";", encoding = 'latin-1')
    ListeAll = pd.concat([ListeAll, Liste], axis=0)

ListeAll.to_csv('Output\\BERUFENET_Berufe_A-Z.csv', sep=";", encoding = 'latin-1')
