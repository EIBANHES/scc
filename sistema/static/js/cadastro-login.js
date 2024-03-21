const cnpjInput = document.getElementById("cnpj");
const razaoCnpj = document.getElementById("hidden-razao");

cnpjInput.addEventListener("blur", (e) => {
    const cnpjInputValue = cnpjInput.value
    if (cnpjInputValue.trim() !== "") {
        razaoCnpj.style.display = "block";
    } else {
        razaoCnpj.style.display = "none";
    }
})