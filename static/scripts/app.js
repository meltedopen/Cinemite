$(function () {
  // let key = "bcd90145aa0a9afa766db2577135dbf4";
  $('.search').on('submit', function (e) {
    e.preventDefault();
    $('.movie-gallery').empty();
    let inputVal = $('.movie-input').val();
    let formattedInput = inputVal.replace(/ /g, '+');
    let movieGallery = $('.movie-gallery');
    let tmdbUrl = "https://api.themoviedb.org/3/search/movie?api_key=bcd90145aa0a9afa766db2577135dbf4&query=" + formattedInput + "&language=en-US&page=1&include_adult=false";

    $.ajax({
      method: 'GET',
      url: tmdbUrl,
      success: function (response) {
        console.log(response);
        response.results.map(child => {
          let movieId = child.id; //////////////
          let img = $(`<img class="result-image" data-id="${movieId}" />`);
          let url = "https://image.tmdb.org/t/p/w500" + child.poster_path
          img.attr("src", url)
          movieGallery.append(img);
          return movieId;///////////////////////
        })
      },
      error: function (error) {
        console.log(error);
      }
    });
    // $.ajax({
    //   method: 'POST',
    //   url: //////////,
    //   success: function(response) {

    //   }
    // })
    $('.movie-gallery').on('click', '.result-image', function () {
      console.log(this)
    })
  });
});


// url = https://api.themoviedb.org/3/configuration?api_key=
