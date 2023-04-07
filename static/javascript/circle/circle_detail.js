window.onscroll = function() {
    var element = document.getElementById("recruit_circle_detail");
    var position = element.getBoundingClientRect();
    if (position.top <= 0) {
      var elements = document.getElementsByClassName("card p-2");
      for (var i = 0; i < elements.length; i++) {
        elements[i].style.animation = "fadein 1s";
      }
    }
  };