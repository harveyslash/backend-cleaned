// $(document).ready(function () {
//   $('.carousel').carousel();
// });
// $('.carousel.carousel-slider').carousel({
//   fullWidth: true
// });

var elem = document.querySelector('.main-carousel');
var flkty = new Flickity(elem, {
  // options
  prevNextButtons: false,
  imagesLoaded: true,
  draggable: true,
  pageDots: false,
  autoPlay: 1500,
  wrapAround: true,
  pauseAutoPlayOnHover: true
});

var elem2 = document.querySelector('.main-carousel-2');
var flkty2 = new Flickity(elem2, {
  // options
  prevNextButtons: false,
  imagesLoaded: true,
  draggable: true,
  pageDots: false,
  autoPlay: 1500,
  wrapAround: true,
  pauseAutoPlayOnHover: true
});

var elem3 = document.querySelector('.main-carousel-3');
var flkty3 = new Flickity(elem3, {
  // options
  imagesLoaded: true,
  draggable: true,
  pageDots: false,
  autoPlay: 1500,
  wrapAround: true,
  pauseAutoPlayOnHover: true
});
