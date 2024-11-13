import json
from collections import defaultdict
import math

def procesare(text):
    text = text.lower().split()
    cuvinte = [x.strip(" ,.?!:;") for x in text]
    stop = {'este', 'sunt', 'o', 'a', 'avut', 'fost', 'au', 'poate', 'face', 'pot', 'include', 'există', 'are',
            'au', 'la', 'de', 'în', 'cu', 'pe', 'între', 'pentru', 'și', 'dar', 'sau', 'iar', 'că', 'acest', 'aceasta',
            'aceste', 'acestuia', 'care', 'unde', 'unul', 'una', 'într-un', 'într-o', 'precum', 'astfel', 'fiecare',
            'despre'}
    return [cuv for cuv in cuvinte if cuv not in stop]

def incarca(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)

def frecvente(date):
    frecv = defaultdict(lambda: defaultdict(int))
    num_art = defaultdict(int)
    total_cuv = defaultdict(int)

    for art in date['articole']:
        cat = art['categorie']
        num_art[cat] += 1
        cuvinte = procesare(art['continut'])
        for cuv in cuvinte:
            frecv[cat][cuv] += 1
            total_cuv[cat] += 1

    return frecv, num_art, total_cuv

def probabilitati(frecv, num_art, total_cuv):
    apriori = {cat: cnt / sum(num_art.values()) for cat, cnt in num_art.items()}
    total_unice = len(set(cuv for f in frecv.values() for cuv in f))
    prob_cuv = defaultdict(lambda: defaultdict(float))

    for cat, cuv_frec in frecv.items():
        total = total_cuv[cat]
        for cuv, freq in cuv_frec.items():
            prob_cuv[cat][cuv] = (freq + 1) / (total + total_unice)

    return apriori, prob_cuv

def clasifica(text, apriori, prob_cuv):
    cuvinte = procesare(text)
    log_prob = {cat: math.log(apriori[cat]) for cat in prob_cuv.keys()}

    for cat in prob_cuv.keys():
        for cuv in cuvinte:
            prob = prob_cuv[cat].get(cuv, 0.00001)
            log_prob[cat] += math.log(prob)

    return max(log_prob, key=log_prob.get)

