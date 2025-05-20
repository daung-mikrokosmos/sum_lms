const backBtn = document.querySelector('#back-button');


$(function() {
    setTimeout(function() {
        $('.alert-msg').fadeOut('slow');
    }, 3000);
    $('[data-bs-toggle="tooltip"]').tooltip();
});


if (backBtn) {
    backBtn.addEventListener('click', function(e) {
        window.history.back();
    })
}