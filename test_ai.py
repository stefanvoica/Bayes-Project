import json
import matplotlib.pyplot as plt
from bayes import incarca, clasifica, frecvente, probabilitati

def citeste_json(cale):
    with open(cale, 'r', encoding='utf-8') as fisier:
        return json.load(fisier)["articole"]

def evalueaza(f_intrare, f_iesire):
    date = incarca(f_intrare)
    frecv, n_art, total_cuv = frecvente(date)
    apriori, prob_cuv = probabilitati(frecv, n_art, total_cuv)

    articole_test = citeste_json(f_iesire)
    corecte = 0
    total = len(articole_test)

    for art in articole_test:
        cat_real = art['categorie']
        continut = art['continut']
        cat_prezisa = clasifica(continut, apriori, prob_cuv)

        if cat_real == cat_prezisa:
            corecte += 1

    acuratete = (corecte / total) * 100
    print(f"Acuratețea pentru {f_intrare}: {acuratete:.2f}%")
    return acuratete

def grafic_acuratete(valori, etichete):
    plt.figure(figsize=(10, 6))
    plt.bar(etichete, valori, color='red')
    plt.xlabel('Seturi de Date')
    plt.ylabel('Acuratețe (%)')
    plt.title('Acuratețea Modelului pe Date de Test')
    plt.ylim(0, 100)
    plt.show()

acuratete = []
etichete = []

for i in range(2, 6):
    f_intrare = f"intrare{i}.json"
    f_iesire = f"iesire{i}.json"

    acc = evalueaza(f_intrare, f_iesire)
    acuratete.append(acc)
    etichete.append(f'Set {i}')

grafic_acuratete(acuratete, etichete)