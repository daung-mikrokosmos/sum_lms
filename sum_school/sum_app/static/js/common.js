const backBtn = document.querySelector('#back-button');


$(function() {
    setTimeout(function() {
        $('.alert-msg').fadeOut('slow');
    }, 3000);
    $('[data-bs-toggle="tooltip"]').tooltip();

    $(".clickable-row").click(function() {
        const href = $(this).data("href");
        if (href) {
            window.location = href;
        }
    });
});


if (backBtn) {
    backBtn.addEventListener('click', function(e) {
        window.history.back();
    })
}