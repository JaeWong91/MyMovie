$(document).ready(function () {
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.modal').modal();
    $('#textarea1').val('New Text');
    M.textareaAutoResize($('#textarea1'));
});

function goBack() {
  window.history.back();
}

// Movie Rating Slider - Taken from w3 schools
var slider = document.getElementById("review_rating");
var output = document.getElementById("review_output");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  output.innerHTML = this.value;
}