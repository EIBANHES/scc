// Alerta
document.addEventListener("DOMContentLoaded", function () {
  let alerts = document.querySelectorAll(".alert");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.remove();
    }, 2400);
  });
});

// Mascara celular
$(document).ready(function () {
  var SPMaskBehavior = function (val) {
    return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
  },
    spOptions = {
      onKeyPress: function (val, e, field, options) {
        field.mask(SPMaskBehavior.apply({}, arguments), options);
      }
    };

  $('#celular-principal, #celular-secundario, #numero-contato').mask(SPMaskBehavior, spOptions);
});

// Form validator bootstrap
(function () {
  'use strict';
  var forms = document.querySelectorAll('.needs-validation');
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
})();

//Script para passar os dados do back-end pelo clique do botão
document.getElementById("generate-btn").addEventListener("click", () => {
  // Abre o modal
  $('#confirmationModal').modal('show');

  // Quando o usuário clicar no botão de confirmação, comecará a operação
  document.getElementById("confirmBtn").addEventListener("click", async () => {
    // Fecha o model e procede
    $('#confirmationModal').modal('hide');

    try {
      const response = await fetch("/pagamentos/gerar/boleto", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ /* */ })
      });

      const data = await response.json();

      if (response.ok) {
        // Redireciona para a página de pagamento com os dados corretos
        window.location.href = `/pagamentos/boleto?pdf_link=${data.pdf_link}&barcode=${data.barcode}&visualizar_pdf=${data.visualizar_pdf}`;
      } else {
        console.error("Error:", data.error);
      }
    } catch (error) {
      console.error("Error:", error.message);
    }
  });
});

// Script para copiar o conteúdo do botão (código de barras)
const copiarButton = document.getElementById('copiarButton');
const copiadoButton = document.getElementById('copiadoButton');
const barcode = new URLSearchParams(window.location.search).get("barcode"); // Pegando o código de barras enviado pela URL

copiarButton.addEventListener('click', () => {
  copiarCodigoBarras(barcode);

  copiarButton.style.display = 'none';
  copiadoButton.style.display = 'inline-block';

  setTimeout(() => {
    copiarButton.style.display = 'inline-block';
    copiadoButton.style.display = 'none';
  }, 3000);
});

function copiarCodigoBarras(text) {
  const textArea = document.createElement('textarea');
  textArea.value = text;
  document.body.appendChild(textArea);
  textArea.select();
  document.execCommand('copy');
  document.body.removeChild(textArea);
}

//Script para visualizar/esconder um container ao usuário clicar no botão
const visualizarButton = document.getElementById('visualizarButton');
const billetInfoContainer = document.getElementById('billetInfoContainer');

visualizarButton.addEventListener('click', () => {
  // Mudando a visibilidade do container (visualizar/esconder)
  if (billetInfoContainer.style.display === 'none' || billetInfoContainer.style.display === '') {
    billetInfoContainer.style.display = 'block';
    visualizarButton.innerHTML = '<i class="fa-sharp fa-light fa-magnifying-glass-minus"></i> Esconder boleto';

    // Get the 'visualizarPdf' value from the URL query parameter
    const visualizarPdf = new URLSearchParams(window.location.search).get("visualizar_pdf");

    // Set the 'src' attribute of the <embed> element to 'visualizarPdf'
    const embedElement = document.querySelector('#billetInfoContainer embed');
    embedElement.src = visualizarPdf;
  } else {
    billetInfoContainer.style.display = 'none';
    visualizarButton.innerHTML = '<i class="fa-sharp fa-light fa-magnifying-glass-plus"></i> Visualizar boleto';
  }
});

//Script para redirecionar para uma página com target blank (nova guia) de acordo com o link do back-end
document.getElementById("imprimirButton").addEventListener("click", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const pdfLink = urlParams.get('pdf_link');

  if (pdfLink) {
    window.open(pdfLink, '_blank');
  } else {
    console.error("'pdf_link' não foi encontrado na URL.");
  }
});

// Script copia e cola chave Pix
document.addEventListener("DOMContentLoaded", function () {
  var botaoCopiar = document.querySelector('.botao-transparente');
  var botaoCopiado = document.querySelector('.botao-transparente.hidden');
  var codigoElement = document.querySelector('.codigo');
  var codigo = codigoElement.textContent;

  botaoCopiar.addEventListener('click', function () {
    var tempInput = document.createElement('input');
    tempInput.value = codigo;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);

    botaoCopiar.classList.add('hidden');
    botaoCopiado.classList.remove('hidden');

    setTimeout(function () {
      botaoCopiado.classList.add('hidden');
      botaoCopiar.classList.remove('hidden');
    }, 3000);
  });
});