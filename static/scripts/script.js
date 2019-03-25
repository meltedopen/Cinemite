// scripts

$(document).ready(function() {
  // curent year
  $('#year').text(new Date().getFullYear());

  // slider config
  $('.carousel').carousel({
    interval: 3000,
    pause: false
  });

  $('.port-item').click(function() {
    $('.collapse').collapse('hide');
  });
});
