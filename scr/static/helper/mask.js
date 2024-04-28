var cpfField = document.getElementById("cpf");
var telefoneField = document.getElementById("telefone");

cpfField.addEventListener("input", function () {
    this.value = this.value
        .replace(/\D/g, "")
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
});

telefoneField.addEventListener("input", function () {
    this.value = this.value
        .replace(/\D/g, "")
        .replace(/(\d{2})(\d)/, "($1) $2")
        .replace(/(\d{4})(\d{1,4})$/, "$1-$2");
});