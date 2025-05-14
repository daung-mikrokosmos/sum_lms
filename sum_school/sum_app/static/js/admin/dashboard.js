$(document).ready(function () {
    $('#program-search').on('keyup', function () {
        const value = $(this).val().toLowerCase();
        $('.program-item').filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });
});