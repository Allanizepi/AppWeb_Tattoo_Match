// Seleciona todos os itens do menu
const itensMenu = document.querySelectorAll('.menu-item');
const galeria = document.getElementById('galeria');

// Função para limpar e exibir novas imagens
function mostrarImagens(tipo, nome) {
  galeria.innerHTML = ''; // limpa galeria anterior

  // Caminho base para as imagens
  let caminhoBase = '';
  if (tipo === 'tamanho') {
    caminhoBase = `imagens/tamanhos/${nome}/`;
  } else {
    caminhoBase = `imagens/estilos/${nome}/`;
  }

  // Exemplo: mostrar 4 imagens (ajuste conforme necessário)
  for (let i = 1; i <= 4; i++) {
    const img = document.createElement('img');
    img.src = `${caminhoBase}${i}.jpg`;
    img.alt = `${nome} ${i}`;
    img.classList.add('img-galeria');
    galeria.appendChild(img);
  }
}

// Adiciona evento de clique a cada item
itensMenu.forEach(item => {
  item.addEventListener('click', () => {
    const nome = item.getAttribute('name');
    const tipo = item.classList.contains('tamanho') ? 'tamanho' : 'estilo';
    mostrarImagens(tipo, nome);
  });
});

