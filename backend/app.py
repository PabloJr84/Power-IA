from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import joblib
import os  # Importe a biblioteca os para manipulação de caminhos

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://IAPowerBI:IA@161207@localhost/inovac68_IA_PowerBI'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definir o caminho para a pasta do modelo de forma mais robusta
MODEL_FOLDER = os.path.join(os.path.dirname(__file__), 'ml_model')
MODEL_FILE = 'powerbi_problem_classifier.pkl'
VECTORIZER_FILE = 'tfidf_vectorizer.pkl'
MODEL_PATH = os.path.join(MODEL_FOLDER, MODEL_FILE)
VECTORIZER_PATH = os.path.join(MODEL_FOLDER, VECTORIZER_FILE)

# Carregar o modelo treinado e o vetorizador
modelo_ia = None
vetorizador = None
try:
    modelo_ia = joblib.load(MODEL_PATH)
    vetorizador = joblib.load(VECTORIZER_PATH)
    print("Modelo e vetorizador carregados com sucesso!")
    print(f"Modelo carregado de: {MODEL_PATH}")
    print(f"Vetorizador carregado de: {VECTORIZER_PATH}")
except FileNotFoundError:
    print(f"Erro: Arquivos do modelo não encontrados em:")
    print(f"- Modelo: {MODEL_PATH}")
    print(f"- Vetorizador: {VECTORIZER_PATH}")

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
    print("Rota /api/ajuda foi acessada com método POST.")
    try:
        data = request.get_json()
        print("Dados da requisição:", data)
        pergunta = data.get('pergunta')
        print("Pergunta recebida:", pergunta)

        if not pergunta:
            print("Erro: A pergunta está vazia.")
            return jsonify({'erro': 'A pergunta não pode estar vazia.'}), 400

        resposta_ia = "Resposta da IA (padrão)."
        categoria_prevista = None

        if modelo_ia and vetorizador:
            print("Modelo e vetorizador estão carregados. Tentando prever...")
            from backend.ml_model.model import prever_problema  # Importar aqui para evitar dependência circular
            categoria_prevista = prever_problema(modelo_ia, vetorizador, pergunta)
            print("Categoria prevista:", categoria_prevista)
            resposta_ia = f"A categoria prevista para sua pergunta é: {categoria_prevista}. (Implemente a lógica para a solução)."
        else:
            print("Modelo ou vetorizador não carregados. Usando resposta padrão.")
            resposta_ia = f"Resposta da IA para: '{pergunta}' (Modelo de IA não carregado)."

        novo_registro = Problema(descricao=pergunta, solucao=resposta_ia)
        db.session.add(novo_registro)
        db.session.commit()
        print("Pergunta e resposta salvas no banco de dados.")

        print("Enviando resposta:", jsonify({'resposta': resposta_ia, 'categoria': categoria_prevista}))
        return jsonify({'resposta': resposta_ia, 'categoria': categoria_prevista})

    except Exception as e:
        db.session.rollback()
        print(f"Erro na rota /api/ajuda: {e}")
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
