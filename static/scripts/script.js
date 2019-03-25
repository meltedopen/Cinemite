// scripts

$(document).ready(function() {
  // curent year
  $('#year').text(new Date().getFullYear());

  // slider config
  $('.carousel').carousel({
    interval: 4000,
    pause: false
  });
});
