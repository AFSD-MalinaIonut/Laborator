meniu = ['papanasi'] * 10 + ['ceafa'] * 3 + ["guias"] * 6
preturi = {"papanasi": 7, "ceafa": 10, "guias": 5}
studenti = ["Liviu", "Ion", "George", "Ana", "Florica"]
comenzi = ["guias", "ceafa", "ceafa", "papanasi", "ceafa"]
tavi = ["tava"] * 7
istoric_comenzi = []

def procesare_comenzi(studenti, comenzi, tavi, istoric_comenzi):
    while studenti and comenzi:
        student, comanda = studenti.pop(0), comenzi.pop(0)
        print(f"{student} a comandat {comanda}.")
        if tavi:
            tavi.pop()
        istoric_comenzi.append(comanda)

def calculeaza_inventar(istoric_comenzi, meniu):
    return {produs: istoric_comenzi.count(produs) for produs in set(meniu)}

def verifica_stocuri(meniu, inventar):
    return {produs: meniu.count(produs) - inventar.get(produs, 0) > 0 for produs in set(meniu)}

def calculeaza_incasari(istoric_comenzi, preturi):
    return sum(preturi[comanda] for comanda in istoric_comenzi)

procesare_comenzi(studenti, comenzi, tavi, istoric_comenzi)

print("\n1. Comenzi procesate:")
print("Istoric comenzi:", istoric_comenzi)

inventar = calculeaza_inventar(istoric_comenzi, meniu)
for produs, cantitate in inventar.items():
    print(f"S-au comandat {cantitate} {produs}.")
print(f"Mai sunt {len(tavi)} tavi.")

stocuri = verifica_stocuri(meniu, inventar)
for produs, disponibil in stocuri.items():
    print(f"Mai sunt {produs}: {disponibil}.")

incasari_totale = calculeaza_incasari(istoric_comenzi, preturi)
produse_ieftine = [produs for produs, pret in preturi.items() if pret <= 7]

print("\n3. Finanțe:")
print(f"Cantina a încasat: {incasari_totale} lei.")
print("Produse care costă cel mult 7 lei:", produse_ieftine)
