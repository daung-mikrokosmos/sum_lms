$(document).ready(function () {
    $('#toggle-password').on('click', function (e) {
        e.preventDefault();
        const field = $('#password');
        const isVisible = field.attr('type') === 'text';
        field.attr('type', isVisible ? 'password' : 'text');
        $('#eye-visible').toggleClass('d-none').toggleClass('d-block');
        $('#eye-hidden').toggleClass('d-none').toggleClass('d-block');
    });
});