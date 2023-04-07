window.onload = function () {
    var section = document.getElementsByTagName("section");
    var pointBtn = document.querySelectorAll(".pointWrap li");
    var pointWrap = document.querySelector(".pointWrap");
    var pageNum = 0;
    var totalNum = section.length;
    var scheduleSection = document.getElementById("schedule");
    var boothSection = document.getElementById("booth");
    var boothCards = boothSection.querySelectorAll(".card");
  
    const boothElem = document.querySelector("#booth");
    const searchFormElem = boothElem.querySelector(".search-form");

    // Samsung 브라우저에서 접속한 경우에만 HTML 코드 변경
    // if (navigator.userAgent.match(/SamsungBrowser/i)) {
    //   searchFormElem.innerHTML = "<button  onclick='window.location.href = '/search''>부스 검색하기</button>";
    // }

    for (var i = 0; i < pointBtn.length; i++) {
      (function (idx) {
        pointBtn[idx].onclick = function () {
          pageNum = idx;
          pageChangeFunc();
          window.scrollTo({
            top: section[pageNum].offsetTop + section[pageNum].offsetHeight / 2 - window.innerHeight / 2,
            behavior: "smooth",
          });
        };
      })(i);
    }
  
    function toggleScroll() {
      const intro = document.getElementById("intro");
      const scroll = document.querySelector(".scroll");
      const halfIntroHeight = intro.offsetHeight / 2;
  
      if (window.scrollY > halfIntroHeight) {
        scroll.style.display = "none";
      } else {
        scroll.style.display = "block";
      }
    }
  
    function initFunc() {
      section[0].classList.add("active");
      pointBtn[0].classList.add("active");
      window.scrollTo(0, document.getElementById("intro").offsetTop);
    }
    initFunc();
  
    window.addEventListener("scroll", function (event) {
      toggleScroll();
      var scroll = this.scrollY;
  
      for (var i = 0; i < totalNum; i++) {
        if (
          scroll > section[i].offsetTop - window.outerHeight / 1.5 &&
          scroll <
            section[i].offsetTop - window.outerHeight / 1.5 + section[i].offsetHeight
        ) {
          pageNum = i;
          break;
        }
      }
      pageChangeFunc();
    });
  
    function pageChangeFunc() {
      for (var i = 0; i < totalNum; i++) {
        section[i].classList.remove("active");
        pointBtn[i].classList.remove("active");
      }
      section[pageNum].classList.add("active");
      pointBtn[pageNum].classList.add("active");
  
      if (pointWrap) {
        if (scrollY > 100) {
          pointWrap.style.display = "block";
        } else {
          pointWrap.style.display = "none";
        }
      }
  
      if (boothSection.classList.contains("active")) {
        boothCards.forEach((card, idx) => {
          setTimeout(() => {
            card.classList.add("show");
          }, 200 * idx);
        });
      } else if (window.scrollY < boothSection.offsetTop) { // 추가
        boothCards.forEach((card) => {
          card.classList.remove("show");
        });
      }
  
      const eventSection = document.getElementById("event");
      const eventCards = eventSection.querySelectorAll(".card");
  
      if (eventSection.classList.contains("active")) {
        eventCards.forEach((card) => {
          card.classList.add("visible");
        });
      } else if (window.scrollY < eventSection.offsetTop) { // 추가
        eventCards.forEach((card) => {
          card.classList.remove("visible");
        });
      }
    }
  
    pageChangeFunc();
    function toggleFloatingBtn() {
        const floatingBtn = document.getElementById("floatingBtn");
        if (window.scrollY > 100) {
            floatingBtn.style.display = "block";
        } else {
            floatingBtn.style.display = "none";
            // 스크롤이 맨 위에 도달하면 다시 애니메이션이 적용되도록 함
            if (boothSection.classList.contains("active")) {
                boothCards.forEach((card, idx) => {
                    setTimeout(() => {
                        card.classList.add("show");
                    }, 200 * idx);
                });
            }
        }
    }
    
    window.addEventListener("scroll", toggleFloatingBtn);
    
    const floatingBtn = document.getElementById("floatingBtn");
    floatingBtn.addEventListener("click", function () {
        window.scrollTo({
            top: 0,
            behavior: "smooth",
        });
    });
}    
