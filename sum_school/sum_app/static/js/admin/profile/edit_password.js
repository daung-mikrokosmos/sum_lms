$(document).ready(function () {
    $('#toggle-old-password').on('click', function (e) {
        e.preventDefault();
        const field = $('#old-password');
        const isVisible = field.attr('type') === 'text';
        field.attr('type', isVisible ? 'password' : 'text');
        $('#old-eye-visible').toggleClass('d-none').toggleClass('d-block');
        $('#old-eye-hidden').toggleClass('d-none').toggleClass('d-block');
    });

    $('#toggle-new-password').on('click', function (e) {
        e.preventDefault();
        const field = $('#new-password');
        const isVisible = field.attr('type') === 'text';
        field.attr('type', isVisible ? 'password' : 'text');
        $('#new-eye-visible').toggleClass('d-none').toggleClass('d-block');
        $('#new-eye-hidden').toggleClass('d-none').toggleClass('d-block');
    });

    $('#toggle-cf-password').on('click', function (e) {
        e.preventDefault();
        const field = $('#cf-password');
        const isVisible = field.attr('type') === 'text';
        field.attr('type', isVisible ? 'password' : 'text');
        $('#cf-eye-visible').toggleClass('d-none').toggleClass('d-block');
        $('#cf-eye-hidden').toggleClass('d-none').toggleClass('d-block');
    });
});
