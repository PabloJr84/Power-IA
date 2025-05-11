import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Coleta e Preparação dos Dados de Treinamento
# Suponha que você tenha um arquivo CSV ou outra fonte de dados
# com colunas 'pergunta' e 'categoria'.
# Exemplo de dados de treinamento atualizado:
data = {
    'pergunta': [
        "Erro ao conectar fonte de dados SQL",
        "Problema com filtro em gráfico de barras",
        "Como criar uma medida de média móvel?",
        "Relatório lento para carregar",
        "Não consigo publicar no Power BI Service",
        "Gráfico de pizza com cores incorretas",
        "Erro de credenciais no gateway",
        "Diferença entre filtro de nível de visual e de página",
        "Calculando percentual do total em uma tabela",
        "Problemas de performance com DAX",
        "Erro ao conectar no Databricks",
        "Falha na conexão com o SharePoint",
        "Problemas com o gateway de dados",
        "Lentidão ao acessar dados do Databricks",
        "SharePoint lista não atualiza no Power BI",
        "Configuração do gateway para fontes de dados na nuvem"
    ],
    'categoria': [
        "Conexão de Dados",
        "Visualização",
        "DAX",
        "Performance",
        "Publicação",
        "Visualização",
        "Gateway",
        "Filtros",
        "DAX",
        "Performance",
        "Databricks",
        "SharePoint",
        "Gateway",
        "Databricks",
        "SharePoint",
        "Gateway"
    ]
}

df = pd.DataFrame(data)

# 2. Pré-processamento de Texto e Engenharia de Features
# Usando TF-IDF para converter texto em vetores numéricos
tfidf_vectorizer = TfidfVectorizer(stop_words='portuguese') # Removendo stopwords em português
X = tfidf_vectorizer.fit_transform(df['pergunta'])
y = df['categoria']

# 3. Divisão dos Dados em Treino e Teste
# Separando os dados para avaliar o desempenho do modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Escolha e Treinamento do Modelo
# Usando um modelo de Regressão Logística para classificação
model = LogisticRegression(multi_class='multinomial', solver='lbfgs', random_state=42)
model.fit(X_train, y_train)

# 5. Avaliação do Modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do modelo: {accuracy:.2f}")
print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred))

# 6. Persistência do Modelo Treinado
# Salvando o modelo e o vetorizador para usar posteriormente na API
model_filename = 'powerbi_problem_classifier.pkl'
vectorizer_filename = 'tfidf_vectorizer.pkl'

joblib.dump(model, f'backend/ml_model/{model_filename}')
joblib.dump(tfidf_vectorizer, f'backend/ml_model/{vectorizer_filename}')

print(f"\nModelo treinado e salvo como: backend/ml_model/{model_filename}")
print(f"Vetorizador TF-IDF salvo como: backend/ml_model/{vectorizer_filename}")