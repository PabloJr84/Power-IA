from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # Para suportar caracteres UTF-8
# *** AQUI VOCÊ COLOCARÁ A CONFIGURAÇÃO DO BANCO DE DADOS ***
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://IAPowerBI:IA@161207@localhost/inovac68_IA_PowerBI'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Opcional: desativa avisos
db = SQLAlchemy(app)

class Problema(db.Model):
    __tablename__ = 'Problemas' # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    solucao = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def __init__(self, descricao, solucao):
        self.descricao = descricao
        self.solucao = solucao

# Exemplo de uma rota para receber a pergunta e salvar no banco de dados
@app.route('/api/ajuda', methods=['POST'])
def obter_ajuda():
    try:
        data = request.get_json()
        pergunta = data.get('pergunta')

        if not pergunta:
            return jsonify({'erro': 'A pergunta não pode estar vazia.'}), 400

        # Simulação da resposta da IA
        resposta_ia = f"Resposta da IA para: '{pergunta}' (Esta é uma resposta de teste)."

        # Salvar a pergunta e a resposta no banco de dados
        novo_registro = Problema(descricao=pergunta, solucao=resposta_ia)
        db.session.add(novo_registro)
        db.session.commit()

        return jsonify({'resposta': resposta_ia})

    except Exception as e:
        db.session.rollback() # Em caso de erro, desfaz as alterações na sessão
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)