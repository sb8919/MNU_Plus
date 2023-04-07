
$(document).ready(function () {
  const width = window.innerWidth;
  if (width < 1198) {
    document.getElementById('circle_list').className = "pt-3 pb-5 mx-auto";
    document.getElementById('circle_list').style.width = "90%";
    document.querySelector('.row-select').style.removeProperty('width');
    const bannerImg1 = document.getElementById('bannerImg1');
    bannerImg1.src = 'static/circle/banner/mobile_banner1.png';
  }

  document.getElementById('category-filter').addEventListener('change', filterCards);
  document.getElementById("recruit-filter").addEventListener("change", filterCards);

  function filterCards() {
    const categoryFilter = document.getElementById('category-filter').value;
    const recruitFilter = document.getElementById("recruit-filter").value;
    const cards = document.querySelectorAll('#card-container .card');
    cards.forEach(card => {
      if ((categoryFilter === 'all' || card.dataset.type === categoryFilter) &&
        (recruitFilter === "all" || card.querySelector(".badge.bg-dark").textContent.trim() === recruitFilter)) {
        card.parentElement.classList.remove('d-none');
        card.parentElement.classList.add('d-flex');
      } else {
        card.parentElement.classList.remove('d-flex');
        card.parentElement.classList.add('d-none');
      }
    });
    const visibleCards = document.querySelectorAll('#card-container .card:not(.d-none)');
    if (visibleCards.length === 0) {
      document.getElementById("no-data-msg").style.display = "block";
    } else {
      document.getElementById("no-data-msg").style.display = "none";
    }
  }


});
