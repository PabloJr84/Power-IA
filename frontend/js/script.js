function enviarPergunta() {
    const perguntaInput = document.getElementById('pergunta');
    const respostaArea = document.getElementById('resposta');
    const categoriaArea = document.getElementById('categoria');
    const pergunta = perguntaInput.value;
  
    if (pergunta.trim() !== "") {
      respostaArea.textContent = 'Carregando resposta...';
      categoriaArea.textContent = 'Categoria Prevista: Carregando...';
  
      fetch('/api/ajuda', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ pergunta: pergunta })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`Erro na requisição: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        respostaArea.textContent = data.resposta;
        categoriaArea.textContent = 'Categoria Prevista: ' + (data.categoria || 'Não Prevista');
      })
      .catch(error => {
        console.error('Erro ao enviar pergunta:', error);
        respostaArea.textContent = 'Erro ao obter resposta.';
        categoriaArea.textContent = 'Categoria Prevista: Erro';
        alert('Ocorreu um erro ao enviar a pergunta. Por favor, tente novamente mais tarde.');
      });
  
      perguntaInput.value = ""; // Limpar a caixa de texto após enviar
    } else {
      alert('Por favor, digite sua pergunta.');
    }
  }