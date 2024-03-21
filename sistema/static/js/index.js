window.addEventListener('DOMContentLoaded', (e) => {
  // Obtém os elementos relevantes
  let possui_petElement = document.getElementById('possui_pet');
  let tipo_petElement = document.querySelector('#tipo_pet');
  let visualizacaoElement = document.querySelector('#visualizacao');

  // Função para verificar o valor de possui_pet e aplicar a lógica apropriada
  function verificarPossuiPetValor() {
    if (possui_petElement.value === '1') {
      visualizacaoElement.classList.remove('hidden');
      tipo_petElement.setAttribute('required', 'required');
    } else {
      visualizacaoElement.classList.add('hidden');
      tipo_petElement.removeAttribute('required');
    }
  }

  // Verifica o valor de possui_pet quando a página é carregada
  verificarPossuiPetValor();

  // Adiciona um ouvinte de evento para mudanças no elemento possui_pet
  possui_petElement.addEventListener('change', (e) => {
    verificarPossuiPetValor();
  });
});

// Função para verificar o valor de 'possui_imovel_vinculado' e aplicar a lógica apropriada
window.addEventListener('DOMContentLoaded', (e) => {
  // Obtém os elementos relevantes
  let possui_imovel_vinculadoElement = document.getElementById('possui_imovel_vinculado');
  let imovel_disponivelElement = document.querySelector('#imovel_disponivel');
  let visualizacaoElement = document.querySelector('#visualizacao');

  // Função para verificar o valor de 'possui_imovel_vinculado' e aplicar a lógica apropriada
  function verificarPossuiImovelValor() {
    if (possui_imovel_vinculadoElement.value === '1') {
      visualizacaoElement.classList.remove('hidden');
      imovel_disponivelElement.setAttribute('required', 'required');
    } else {
      visualizacaoElement.classList.add('hidden');
      imovel_disponivelElement.removeAttribute('required');
    }
  }

  // Verifica o valor de 'possui_imovel_vinculado' quando a página é carregada
  verificarPossuiImovelValor();

  // Adiciona um ouvinte de evento para mudanças no elemento 'possui_imovel_vinculado'
  possui_imovel_vinculadoElement.addEventListener('change', (e) => {
    verificarPossuiImovelValor();
  });
});

// Mascara CPF, CNPJ, RG e CPF/CNPJ
$(document).ready(function () {
  $('#cpf').mask('000.000.000-00', { reverse: true });
  $('#rg').mask('0.000.000', { reverse: true });
  $('#cnpj').mask('00.000.000/0000-00', { reverse: true });
  $("#cpfcnpj").on('input', function() {
    var value = $(this).val().replace(/\D/g, '');

    if (value.length <= 11) {
      $(this).mask("000.000.000-009");
    } else {
      $(this).mask("00.000.000/0000-00");
    }
  });
});

// Função para formatação de valor numérico
function formatarValorNumerico(num) {
  // Substitui a vírgula por ponto como separadorr
  num = num.replace('.', '').replace(',', '.');

  // Remove caracteres, com exceção de núm e '.'
  num = num.replace(/[^0-9.]/g, '');

  // Verifica se o valor é vazio ou um NaN (número inválido ou nao identificado)
  if (num === '' || isNaN(num)) {
    num = '0';
  }

  return num;
}

// Função para atualizar o campo de valor total
function atualizarValorTotal() {
  var valor = document.getElementById('produtoValor').value;
  var estoque = document.getElementById('produtoEstoque').value;

  valor = formatarValorNumerico(valor);
  estoque = formatarValorNumerico(estoque);

  var valorTotal = valor * estoque || 0;

  document.getElementById('produtoValorTotal').value = valorTotal.toFixed(2).replace('.', ',');
}

// Atualizar o valor total ao modificar os campos de valor e estoque
document.getElementById('produtoValor').addEventListener('input', atualizarValorTotal);
document.getElementById('produtoEstoque').addEventListener('input', atualizarValorTotal);

//Evento para validar se o primeiro valor informado no campo de valor e estoque não são caracteres além de numeros:

document.getElementById('produtoValor').addEventListener('keypress', function (event) {
  // Regex que verifica se o primeiro dígito digitado não é um número
  if (this.value === '' && !/[0-9]/.test(event.key)) {
    event.preventDefault();
  } else {
    // Regex que verifica se o caractere digitado não é um número, ',' ou '.'
    if (!/[0-9.,]/.test(event.key)) {
      event.preventDefault();
    }
  }
});

document.getElementById('produtoEstoque').addEventListener('keypress', function (event) {
  // Regex que verifica se o primeiro dígito digitado não é um número
  if (this.value === '' && !/[0-9]/.test(event.key)) {
    event.preventDefault();
  } else {
    // Regex que verifica se o caractere digitado não é um número, ',' ou '.'
    if (!/[0-9.,]/.test(event.key)) {
      event.preventDefault();
    }
  }
});