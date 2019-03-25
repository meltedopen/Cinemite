$(function() {
  // let key = "bcd90145aa0a9afa766db2577135dbf4";
  $('.search').on('submit', function(e) {
    console.log('on submit');
    e.preventDefault();

    $('.movie-gallery').empty();
    let inputVal = $('.movie-input').val();
    let formattedInput = inputVal.replace(/ /g, '+');
    let movieGallery = $('.movie-gallery');
    let tmdbUrl =
      'https://api.themoviedb.org/3/search/movie?api_key=bcd90145aa0a9afa766db2577135dbf4&query=' +
      formattedInput +
      '&language=en-US&page=1&include_adult=false';

    $.ajax({
      method: 'GET',
      url: tmdbUrl,
      success: function(response) {
        console.log(response);
        response.results.map(child => {
          let movieId = child.id;
          let card = $(`<div class="card search-wrapper"/>`);
          let img = $(`<img class="result-image" />`);
          let imgWrapper = $(`<div class="search-image-wrapper" />`);
          let btn = $(
            `<input class="result-button btn btn-dark btn-block" type=submit value="Add To List" data-id="${movieId}"></input>`
          );
          let url = 'https://image.tmdb.org/t/p/w500' + child.poster_path;
          img.attr('src', url);
          imgWrapper.append(img);
          card.append(imgWrapper, btn);
          if (child.poster_path) {
            movieGallery.append(card);
          }
          return movieId;
        });
      },
      error: function(error) {
        console.log(error);
      }
    });
  });

  $('.movie-gallery').on('click', '.result-button', function(e) {
    let clickedMovieId = e.target.getAttribute('data-id');
    $.ajax({
      method: 'POST',
      url: `http://localhost:8000/movie/${clickedMovieId}`,
      success: function(res) {
        console.log(`Clicked Movie ID was successfully added to DB: ${res}`);
      },
      error: function(error) {
        console.log(error);
      }
    });
  });

  $('.now-playing').on('click', '.now-playing-button', function(e) {
    console.log('You clicked on a movie');
    let clickedMovieId = e.target.getAttribute('data-id');
    $.ajax({
      method: 'POST',
      url: `http://localhost:8000/movie/${clickedMovieId}`,
      success: function(res) {
        console.log(`Clicked Movie ID was successfully added to DB: ${res}`);
      },
      error: function(error) {
        console.log(error);
      }
    });
  });
});

// url = https://api.themoviedb.org/3/configuration?api_key=
