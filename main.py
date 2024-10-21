import pandas as pd
import random

def data_lezen() -> tuple:
    data = pd.read_csv("klasgroepen.csv")
    
    column_titles = data.columns
    klas_groepen = data.klasgroep.unique().tolist()
    mct_studenten = data[data.klasgroep.str.contains("MCT")]
    ctai_studenten = data[data.klasgroep.str.contains("CTAI")]
    aantal_studenten_in_klas = {}

    for i in range(len(klas_groepen)):
        aantal_studenten_in_klas[klas_groepen[i]] = data[data.klasgroep == klas_groepen[i]]
    return (column_titles, klas_groepen, mct_studenten, ctai_studenten, aantal_studenten_in_klas, data)

def samenvatting_printen(klas_groepen, mct_studenten, ctai_studenten, aantal_studenten_in_klas) -> None:
    print()
    print(f"Er zijn {len(klas_groepen)} klasgroepen van MCT an CTAI")

    for i in range(len(aantal_studenten_in_klas)):
        print(f"Er zijn {len(aantal_studenten_in_klas[klas_groepen[i]])} studenten in {klas_groepen[i]}")

    print(f"Er zijn {len(mct_studenten)} studenten in MCT")
    print(f"Er zijn {len(ctai_studenten)} studenten in CTAI")
    print()

def studenten_willekeurig_verdelen(groeps_grotte: int, data: tuple) -> None:
    
    mct_studenten_list = data[2].values
    ctai_studenten_list = data[3].values
    column_title = data[0].tolist()
    klas_groepen = data[1]
    alle_studenten_lijst = data[-1]
    
    print()
    print("Jij kan kiezen tussen:\n     A)Het groepje bestaan uit x-aantal willekeurige studenten uit MCT én CTAI\n     B)Het groepje bestaan uit x-aantal willekeurige studenten van enkel MCT of van enkel CTAI\n     C)Het groepje bestaan uit x-aantal willekeurige studenten van 1 klasgroep (bv 1MCT3 )\n     D)Het groepje bestaan uit x-aantal willekeurige studenten van verschillendeklasgroepen (bv 1MCT3 én 1MCT4 én 1CTAI2)")
    
    keuze = input("Wat is u keuze: ").strip().lower()
    groepje = []
    
    if keuze == "a":
        random.shuffle(mct_studenten_list)
        random.shuffle(ctai_studenten_list)
        
        aantal_mctiers = round(groeps_grotte / 2)
        aantal_ctaiers = round(groeps_grotte - aantal_mctiers)
        
        groepje = mct_studenten_list[: aantal_mctiers].tolist() + ctai_studenten_list[: aantal_ctaiers].tolist()
        groepje = pd.DataFrame(data=groepje, columns=column_title)
        
        with open("groepje_van_mct&ctai.csv", "w") as file:
            file = groepje.to_csv("groepje_van_mct&ctai.csv", mode="w", index= False)
    if keuze == "b":
        klas = input("Van welke klas wilt u MCT(M) of CTAI(C): ").strip().lower()
        if klas == "m":
            random.shuffle(mct_studenten_list)
            aantal_mctiers = round(groeps_grotte)
            groepje = mct_studenten_list[: aantal_mctiers].tolist()
            groepje = pd.DataFrame(data=groepje, columns=column_title)
            with open("groepje_van_mct.csv", "w") as file:
                file = groepje.to_csv("groepje_van_mct.csv", mode="w", index= False)
        elif klas == "c":
            random.shuffle(mct_studenten_list)
            aantal_ctaiers = round(groeps_grotte)
            groepje = mct_studenten_list[: aantal_ctaiers].tolist()
            groepje = pd.DataFrame(data=groepje, columns=column_title)
            with open("groepje_van_ctai.csv", "w") as file:
                file = groepje.to_csv("groepje_van_ctai.csv", mode="w", index= False)
    if keuze == "c":
        print("Van welke Klasgroep wil jij een groepje maken: ")
        for i in range(len(klas_groepen)):
            print(f"\t  {i + 1}) Voor klasgorep {klas_groepen[i]}")
        keuze = int(input("geef het klasgroeps nummer: ").strip())
        gekozen_klas_groep = alle_studenten_lijst[alle_studenten_lijst.klasgroep.str.contains(klas_groepen[keuze - 1])].values.tolist()
        random.shuffle(gekozen_klas_groep)
        aantal_studenten = round(groeps_grotte)
        groepje = pd.DataFrame(gekozen_klas_groep[:aantal_studenten], columns=column_title)
        with open("groep_van_1_klas.csv", "w") as file:
            file = groepje.to_csv("groep_van_1_klas", mode="w", index= False)
    
    if keuze == "d":
        aantal_studenten = round(groeps_grotte)
        verschillende_klas_groep = alle_studenten_lijst[: aantal_studenten]
        with open("groepje_van_verschillend_klas_groepen.csv", "w") as file:
            file = groepje.to_csv("groepje_van_verschillend_klas_groepen.csv", mode="w", index= False)
        
def main() -> None:
    keuze = input("Welcome bij samenvattinger, Mogelijke Keuzes\nA) Toon samenvatting\nB) Studenten willekeurige verdelen\nC) Sluiten\nWat is u keuze: ").strip().lower()
    
    if keuze == "a":
        (column_titles, klas_groepen, mct_studenten, ctai_studenten, aantal_studenten_in_klas, data) = data_lezen()
        samenvatting_printen(klas_groepen, mct_studenten, ctai_studenten, aantal_studenten_in_klas)
    elif keuze == "b":
        #groepsgrotte vragen
        groepsgrotte = input("Hoe groot wil jij de groepsgrotte zijn? ").strip().lower()
        studenten_willekeurig_verdelen(int(groepsgrotte), data_lezen())

    
main()