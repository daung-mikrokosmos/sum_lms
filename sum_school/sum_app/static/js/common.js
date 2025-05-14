$(function() {
    setTimeout(function() {
        $('.alert-msg').fadeOut('slow');
    }, 3000);
    $('[data-bs-toggle="tooltip"]').tooltip();
});