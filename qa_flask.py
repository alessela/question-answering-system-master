#BIBLIOGRAFIE
#https://colab.research.google.com/github/huggingface/notebooks/blob/master/examples/question_answering.ipynb#scrollTo=n9qywopnIrJH
#https://intersog.com/blog/the-basics-of-qa-systems-from-a-single-function-to-a-pre-trained-nlp-model-using-python/

from flask import Flask, redirect, url_for, request,render_template
import question_answering_system as qa

#Aless si Alexandra - qa_flask.py

#Flask este un microframework web pentru aplicatii web
#el returneaza un template web cu contextul dat
#declaram aplicatia care va fi rulata
app=Flask(__name__)

#Se ruleaza aplicatia de sucess cand se calculeaza un raspuns pentru intrebare
@app.route('/success/answer')
def success():

    return 'welcome %s'

#Functia de login preia intrebarea introdusa de utilizator
#si cauta raspunsul corect sau cel mai apropriat
#data set-ul este printat si in consola
#vom stoca si in scores.csv scorurile calculate
#returneaza pagina answers.html cu raspunsul la intrebarea introdusa

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        test_data=[]
        test_data.append(request.form['tname'])
        print(test_data)

        k = qa.getResults(test_data, qa.getApproximateAnswer2)
        k.to_csv('scores.csv')
        print(k.iloc[0]['A'])
        return render_template('answers.html',value=k.iloc[0]['A'])
        #return redirect(url_for('success', name='answer'))
    else:
        #user = request.args.get('nm')
        #return redirect(url_for('success', name=user))
        return 0

#Apel de functie principala, main
if __name__ == '__main__':
    app.run()
