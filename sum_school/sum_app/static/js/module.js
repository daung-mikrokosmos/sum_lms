const moduleSelect = document.querySelector("#module-selector");

if (moduleSelect) {
  moduleSelect.addEventListener("change", function (e) {
    this.value && location.assign(this.value);
  });
}
