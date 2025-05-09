const moduleSelect = document.querySelector('#module-selector');

moduleSelect.addEventListener('change' , function (e) {
    this.value && location.assign(this.value)
})

