const tagBtnContainer = document.querySelector(".btns");
const restaurantContainer = document.querySelector(".row");
const restaurants = document.querySelectorAll(".col");

tagBtnContainer.addEventListener("click", (event) => {
  const filter =
    event.target.dataset.filter || event.target.parentNode.dataset.filter;
  if (filter == null) {
    return;
  }
  restaurantContainer.classList.add("anim-out");
  setTimeout(() => {
    restaurants.forEach((restaurant) => {
      if (filter === "*" || filter === restaurant.dataset.type) {
        restaurant.style.display = "block";
      } else {
        restaurant.style.display = "none";
      }
    });
    restaurantContainer.classList.remove("anim-out");
  }, 280);
});
