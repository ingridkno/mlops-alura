from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
import pickle
import os
#import pandas as pd

#from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LinearRegression

#url = 'https://raw.githubusercontent.com/alura-cursos/1576-mlops-machine-learning/aula-5/casas.csv'
#df = pd.read_csv(url)
## colunas = ['tamanho', 'preco']
## df = df[colunas]
#colunas = ['tamanho', 'ano', 'garagem']

#X = df.drop('preco', axis=1)
#y = df['preco']
#X_train, X_test, y_train, y_test = train_test_split(X, y, 
#                                                    test_size = 0.3, 
#                                                    random_state=42)
#modelo = LinearRegression()
#modelo.fit(X_train, y_train)
modelo = pickle.load(open('../../models/modelo.sav', 'rb'))
colunas = ['tamanho', 'ano', 'garagem']


app = Flask(__name__)
# app.config['BASIC_AUTH_USERNAME'] = 'julio'
# app.config['BASIC_AUTH_PASSWORD'] = 'alura'
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

@app.route('/')

def home():
    return "Minha primeira API."


@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(to='en')
    polaridade = tb_en.sentiment.polarity
    return "polaridade: {}".format(polaridade)

#@app.route('/cotacao/<int:tamanho>')
#def cotacao(tamanho):
#    preco = modelo.predict([[tamanho]])
#    return str(preco)

@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col]for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco = preco[0])


app.run(debug=True, host='0.0.0.0')