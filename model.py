import joblib

def carregar_modelo(caminho_arquivo):
    return joblib.load(caminho_arquivo)

def prever_problema(modelo, texto_usuario):
    # Aqui você implementaria a lógica para processar o texto do usuário
    # e usar o modelo para fazer uma previsão.
    # Isso pode envolver vetorização do texto, etc.
    # Por enquanto, apenas um exemplo:
    return f"O modelo de IA analisou: '{texto_usuario}' e sugere a seguinte ação (a ser implementada)."

# Exemplo de como treinar e salvar um modelo (isso poderia estar em train.py):
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
#
# corpus = [
#     "erro na conexão com a fonte de dados",
#     "problema ao atualizar o relatório",
#     # ... mais exemplos de problemas e soluções
# ]
#
# solucao = [
#     "verifique as configurações da fonte de dados",
#     "atualize as credenciais ou agende a atualização",
#     # ... soluções correspondentes
# ]
#
# vetorizador = TfidfVectorizer()
# X = vetorizador.fit_transform(corpus)
# y = solucao
#
# modelo = LogisticRegression()
# modelo.fit(X, y)
#
# joblib.dump(modelo, 'meu_modelo.pkl')
# joblib.dump(vetorizador, 'vetorizador.pkl')