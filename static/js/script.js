$(document).ready(function () {
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.modal').modal();
    $('#textarea1').val('New Text');
    M.textareaAutoResize($('#textarea1'));
});