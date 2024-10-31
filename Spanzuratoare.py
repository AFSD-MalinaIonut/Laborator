import random

cuvinte = ["python", "programare", "calculator", "date", "algoritm"]
cuvant_de_ghicit = random.choice(cuvinte)
progres = "_" * len(cuvant_de_ghicit)

incercari_ramase = 6
litere_incercate = set()

print(progres)
print(f"Încercări rămase: {incercari_ramase}")

while incercari_ramase > 0 and "_" in progres:
    litera = input("Introdu o literă: ").lower()

    if len(litera) != 1 or not litera.isalpha():
        print("Introduceți o singură literă validă.")
        continue
    if litera in litere_incercate:
        print("Această literă a fost deja încercată.")
        continue

    litere_incercate.add(litera)

    if litera in cuvant_de_ghicit:
        progres = "".join(
            [litera if cuvant_de_ghicit[i] == litera else progres[i] for i in range(len(cuvant_de_ghicit))])
        print("Litera este corectă!")
    else:
        incercari_ramase -= 1
        print("Litera nu este în cuvânt.")

    print("Progres: " + " ".join(progres))
    print(f"Încercări rămase: {incercari_ramase}")

if "_" not in progres:
    print("Felicitări! Ai ghicit cuvântul:", cuvant_de_ghicit)
else:
    print("Ai pierdut! Cuvântul era:", cuvant_de_ghicit)
