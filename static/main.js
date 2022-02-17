const navBar = document.getElementById("nav")
const questionBtn = document.querySelectorAll(".question-btn")
const topLinks = document.querySelector(".top-link");

window.addEventListener('scroll', function() {
  const scrollHeight = window.pageYOffset;
  const navHeight = navBar.getBoundingClientRect().height;

  if(scrollHeight > navHeight) {
     navBar.classList.add("fixed-nav")
  }
  else {
    navBar.classList.remove("fixed-nav")
  }
})


questionBtn.forEach(function (btn) {
   btn.addEventListener('click', function () {
     const butt = this.parentElement.parentElement
    butt.classList.toggle("show-text")
   })
})


window.addEventListener('scroll', function() {
  const scrollHeight = window.pageYOffset;

  if(scrollHeight > 600) {
       topLinks.classList.add("show-link")
  }
  else {
      topLinks.classList.remove("show-link")
  }

})

const dateEl = document.getElementById("date")
now = new Date().getFullYear()
dateEl.innerHTML = now;