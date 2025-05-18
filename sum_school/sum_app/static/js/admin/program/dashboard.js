function resizeCard() {
    if ($(window).width() > 991) {
        let maxHeight = 0;

        $('.total-card .card').each(function () {
            let height = $(this).outerHeight();
            if (height > maxHeight) {
                maxHeight = height;
            }
        });

        $('.total-card .card').height(maxHeight);
    }

    let icoBoxHeight = $('.total-icon').outerWidth();
    let iconHeight = $('.total-icon .icon').outerWidth();

    $('.total-icon').css('max-height', icoBoxHeight);
    $('.total-icon .icon').css('height', iconHeight);
}

resizeCard();

$(window).on('resize', function () {
    resizeCard();
});