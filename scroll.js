list = document.querySelector(
  "div.v-menu__content.theme--light.menuable__content__active.v-autocomplete__content"
);
// let oldHeight = 0;
// while (oldHeight != list.scrollHeight) {
//   oldHeight = list.scrollHeight;
//   list.scrollTo(0, list.scrollHeight);
// }
let oldHeight = 0;
let scroll_loop = setInterval(() => {
  oldHeight = list.scrollHeight;
  list.scrollTo(0, list.scrollHeight);
  if (oldHeight == list.scrollHeight) {
    clearInterval(scroll_loop);
  }
}, 100);
