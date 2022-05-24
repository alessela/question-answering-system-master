#Alexandra
#pandas este o librarie care se ocupa cu manipularea si analizarea datelor
#re - il import pentru expresii regulate sau regex-uri
#ratio important din Lavenshtein calculeaza rata de similaritate a listei de string-uri transmise
import pandas as pd
import re
from Levenshtein import ratio

#Se citesc datele din fisierele .csv
# in Train.csv se afla perechile Question-Answer ce reprezinta modelul de antrenament
# in Test.csv se afla intrebarile introduse de utilizator
# in test_data vom introduce in lista intrebarile din Test.csv

data = pd.read_csv('Train.csv')

# this function is used to get printable results

test_data_df=pd.read_csv('Test.csv')
test_data=test_data_df["Questions"].to_list()

#Aless
#Functia aceasta afiseaza rezultatele pentru printare
#questions - lista de intrebari
# fn - functie care calculeaza predictia, raspunsul si scorul intrebarii introduse de utilizator
#functia getResults returneaza un tabel cu intrebarile, predictiile, raspunsurile si scorurile corespunzatoare

def getResults(questions, fn):
    def getResult(q):
        answer, score, prediction = fn(q)
        return [q, prediction, answer, score]

    return pd.DataFrame(list(map(getResult, questions)), columns=["Q", "Prediction", "A", "Score"])

#Alexandra
#Regex ne ajuta sa parsam anumite semne de functuatie continute in intrebari
#Verificam ca intrebarea noastra sa nu fie nulla
#In caz de succes vom returna perechea de Raspuns - Intrebare

def getNaiveAnswer(q):
    # regex helps to pass some punctuation signs
    row = data.loc[data['Question'].str.contains(re.sub(r"[^\w'\s)]+", "", q),case=False)]
    if len(row) > 0:
        return row["Answer"].values[0], 1, row["Question"].values[0]
    return "Sorry, I didn't get you.", 0, ""

#Aless
#pentru fiecare intrebare din modelul de antrenare calculeaza scorul generat
#pe baza similaritatii intre intrebarea curenta si intrebarea introdusa de utilizator
#daca scorul este mai mare decat 0.9 atunci ne vom opri (avem deja raspunsul)
#altfel calculam raspunsul cel mai apropriat de raspunsul corect

def getApproximateAnswer2(q):
    max_score = 0
    answer = ""
    prediction = ""
    for idx, row in data.iterrows():
        score = ratio(row["Question"], q)
        if score >= 0.9: # I'm sure, stop here
            return row["Answer"], score, row["Question"]
        elif score > max_score: # I'm unsure, continue
            max_score = score
            answer = row["Answer"]
            prediction = row["Question"]

    if max_score > 0.3: # treshold is lowered
        return answer, max_score, prediction
    return "Sorry, I didn't get you.", max_score, prediction




'''
k=getResults(["What is the population of egypt?"],getNaiveAnswer)
print(k.iloc[0]['A'])
'''

#Alexandra
#Stocam in k rezultatele obtinute si le introducem intr-un scores.csv
k=getResults(test_data,getApproximateAnswer2)
k.to_csv('scores.csv')


