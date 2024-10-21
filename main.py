import pandas as pd #Importeren de pandas Bib
import random #Importenre de Random Bib

def data_lezen() -> tuple:
    '''
    Leest de data uit de "klasgroepen.csv" bestand, en geeft een tuple terug met de volgende lijsten: column_titles, klas_groepen, mct_studenten, ctai_studenten, aantal_studenten_in_klas, data
    '''
    data = pd.read_csv("klasgroepen.csv")  # Lees de CSV-bestand in
    
    # Haal de kolomtitels op
    column_titles = data.columns
    # Haal de unieke klasgroepen op
    klas_groepen = data.klasgroep.unique().tolist() 
    # Filter de MCT-studenten
    mct_studenten = data[data.klasgroep.str.contains("MCT")]
    # Filter de CTAI-studenten
    ctai_studenten = data[data.klasgroep.str.contains("CTAI")]
    aantal_studenten_in_klas = {}

    # Vul de aantal_studenten_in_klas dictionary met de aantal studenten in elke klasgroep
    for i in range(len(klas_groepen)):
        aantal_studenten_in_klas[klas_groepen[i]] = data[data.klasgroep == klas_groepen[i]]
    # Retourneer de verzamelde data als een tuple
    return (column_titles, klas_groepen, mct_studenten, ctai_studenten, aantal_studenten_in_klas, data)

def samenvatting_printen(klas_groepen, mct_studenten, ctai_studenten, aantal_studenten_in_klas) -> None:
    """Functie om een samenvating van de klasgroepen en studenten af te druken"""
    print()
    print(f"Er zijn {len(klas_groepen)} klasgroepen van MCT an CTAI")
    # Loop door elke klasgroep en print het aantal studenten in die klasgroep
    for i in range(len(aantal_studenten_in_klas)):
        print(f"Er zijn {len(aantal_studenten_in_klas[klas_groepen[i]])} studenten in {klas_groepen[i]}")

    print(f"Er zijn {len(mct_studenten)} studenten in MCT")
    print(f"Er zijn {len(ctai_studenten)} studenten in CTAI")
    print()

def studenten_willekeurig_verdelen(groeps_grotte: int, data: tuple) -> None:
    """Functie om gekozen groeps studenten willekeurig in groepen te verdelen."""
    
    # Haal de lijst van MCT-studenten uit de data
    mct_studenten_list = data[2].values
    # Haal de lijst van CTAI-studenten uit de data
    ctai_studenten_list = data[3].values
    # Haal de kolomtitels uit de data
    column_title = data[0].tolist()
    # Haal de klasgroepen uit de data
    klas_groepen = data[1]
    # Haal de volledige lijst van alle studenten uit de data
    alle_studenten_lijst = data[-1]
    
    print()
    print("Jij kan kiezen tussen:\n     A)Het groepje bestaan uit x-aantal willekeurige studenten uit MCT én CTAI\n     B)Het groepje bestaan uit x-aantal willekeurige studenten van enkel MCT of van enkel CTAI\n     C)Het groepje bestaan uit x-aantal willekeurige studenten van 1 klasgroep (bv 1MCT3 )\n     D)Het groepje bestaan uit x-aantal willekeurige studenten van verschillendeklasgroepen (bv 1MCT3 én 1MCT4 én 1CTAI2)")
    
    # Vraag de gebruiker om een keuze te maken
    keuze = input("Wat is u keuze: ").strip().lower()
    groepje = []
    
    if keuze == "a":
        # Schud de lijsten van MCT- en CTAI-studenten willekeurig
        random.shuffle(mct_studenten_list)
        random.shuffle(ctai_studenten_list)
        
        # Bepaal het aantal MCT- en CTAI-studenten in het groepje
        aantal_mctiers = round(groeps_grotte / 2)
        aantal_ctaiers = round(groeps_grotte - aantal_mctiers)
        
        # Combineer de studenten in een groepje en maak er een DataFrame van
        groepje = mct_studenten_list[: aantal_mctiers].tolist() + ctai_studenten_list[: aantal_ctaiers].tolist()
        groepje = pd.DataFrame(data=groepje, columns=column_title)
        
        # Schrijf het groepje naar een CSV-bestand
        with open("groepje_van_mct&ctai.csv", "w") as file:
            file = groepje.to_csv("groepje_van_mct&ctai.csv", mode="w", index= False)
    if keuze == "b":
        # Vraag de gebruiker om een keuze te maken tussen MCT en CTAI
        klas = input("Van welke klas wilt u MCT(M) of CTAI(C): ").strip().lower()
        if klas == "m":
            # Schud de lijst van MCT-studenten willekeurig
            random.shuffle(mct_studenten_list)
            aantal_mctiers = round(groeps_grotte)
            groepje = mct_studenten_list[: aantal_mctiers].tolist()
            
            # Maak er een DataFrame van
            groepje = pd.DataFrame(data=groepje, columns=column_title)
            # Schrijf het groepje naar een CSV-bestand
            with open("groepje_van_mct.csv", "w") as file:
                file = groepje.to_csv("groepje_van_mct.csv", mode="w", index= False)
        elif klas == "c":
            # Schud de lijst van CTAI-studenten willekeurig
            random.shuffle(mct_studenten_list)
            aantal_ctaiers = round(groeps_grotte)
            groepje = mct_studenten_list[: aantal_ctaiers].tolist()
            
            # Maak er een DataFrame van
            groepje = pd.DataFrame(data=groepje, columns=column_title)
            # Schrijf het groepje naar een CSV-bestand
            with open("groepje_van_ctai.csv", "w") as file:
                file = groepje.to_csv("groepje_van_ctai.csv", mode="w", index= False)
    if keuze == "c":
        # Vraag de gebruiker om een klasgroep te kiezen
        print("Van welke Klasgroep wil jij een groepje maken: ")
        for i in range(len(klas_groepen)):
            print(f"\t  {i + 1}) Voor klasgorep {klas_groepen[i]}")
        keuze = int(input("geef het klasgroeps nummer: ").strip())
        # Selecteer de studenten die bij de gekozen klasgroep horen
        gekozen_klas_groep = alle_studenten_lijst[alle_studenten_lijst.klasgroep.str.contains(klas_groepen[keuze - 1])].values.tolist()
        
        # Schud de lijst van gekozen studenten willekeurig
        random.shuffle(gekozen_klas_groep)
        aantal_studenten = round(groeps_grotte)
        groepje = pd.DataFrame(gekozen_klas_groep[:aantal_studenten], columns=column_title)
        # Schrijf het groepje naar een CSV-bestand
        with open("groep_van_1_klas.csv", "w") as file:
            file = groepje.to_csv("groep_van_1_klas", mode="w", index= False)
    
    if keuze == "d":
        # Selecteer 'aantal_studenten' uit de lijst van alle studenten
        aantal_studenten = round(groeps_grotte)
        verschillende_klas_groep = alle_studenten_lijst[: aantal_studenten]
        
        # Schrijf het groepje naar een CSV-bestand
        with open("groepje_van_verschillend_klas_groepen.csv", "w") as file:
            file = groepje.to_csv("groepje_van_verschillend_klas_groepen.csv", mode="w", index= False)
        
def main() -> None:
    """
    Hoofdfunctie om het programma uit te voeren.
    """
    # Vraag de gebruiker om een keuze te maken uit de mogelijke opties
    keuze = input("Welcome bij samenvattinger, Mogelijke Keuzes\nA) Toon samenvatting\nB) Studenten willekeurige verdelen\nC) Sluiten\nWat is u keuze: ").strip().lower()
    
    if keuze == "a":
         # Lees de data en print de samenvatting
        (column_titles, klas_groepen, mct_studenten, ctai_studenten, aantal_studenten_in_klas, data) = data_lezen()
        samenvatting_printen(klas_groepen, mct_studenten, ctai_studenten, aantal_studenten_in_klas)
    elif keuze == "b":
        #groepsgrotte vragen
        groepsgrotte = input("Hoe groot wil jij de groepsgrotte zijn? ").strip().lower()
        studenten_willekeurig_verdelen(int(groepsgrotte), data_lezen())

    
main()