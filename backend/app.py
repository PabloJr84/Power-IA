from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from backend.ml_model.model import prever_problema  # Importe a função prever_problema

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://IAPowerBI:IA@161207@localhost/inovac68_IA_PowerBI'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Carregar o modelo treinado e o vetorizador
modelo_ia = None
vetorizador = None
try:
    modelo_ia = joblib.load('backend/ml_model/powerbi_problem_classifier.pkl')
    vetorizador = joblib.load('backend/ml_model/tfidf_vectorizer.pkl')
except FileNotFoundError:
    print("Erro: Arquivos do modelo não encontrados em backend/ml_model/")

class Problema(db.Model):
    __tablename__ = 'Problemas'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    solucao = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def __init__(self, descricao, solucao):
        self.descricao = descricao
        self.solucao = solucao

@app.route('/api/ajuda', methods=['POST'])
def obter_ajuda():
    try:
        data = request.get_json()
        pergunta = data.get('pergunta')

        if not pergunta:
            return jsonify({'erro': 'A pergunta não pode estar vazia.'}), 400

        resposta_ia = "Resposta da IA (padrão)."
        categoria_prevista = None

        if modelo_ia and vetorizador:
            categoria_prevista = prever_problema(modelo_ia, vetorizador, pergunta)
            resposta_ia = f"A categoria prevista para sua pergunta é: {categoria_prevista}. (Implemente a lógica para a solução)."
        else:
            resposta_ia = f"Resposta da IA para: '{pergunta}' (Modelo de IA não carregado)."

        novo_registro = Problema(descricao=pergunta, solucao=resposta_ia)
        db.session.add(novo_registro)
        db.session.commit()

        return jsonify({'resposta': resposta_ia, 'categoria': categoria_prevista})

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)