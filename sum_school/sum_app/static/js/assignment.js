const backBtn = document.querySelector('#back-button');


if (backBtn) {
    backBtn.addEventListener('click', function(e) {
        window.history.back();
    })
}