const buttonArr = document.getElementsByTagName("button");

for (let i = 0; i < buttonArr.length; i++) {
  buttonArr[i].addEventListener("click", function (e) {
    e.preventDefault();
    document.querySelector(".day" + (i + 1)).scrollIntoView(true);
  });
}
