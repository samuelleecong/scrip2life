// Card Hover Animations
const card = document.querySelector('.card');

card.addEventListener('mouseenter', () => {
  card.style.transform = 'scale(1.05)';
});

card.addEventListener('mouseleave', () => {
  card.style.transform = 'scale(1)';
});

// Loading Animation at Home Page before Page loading
window.addEventListener("load", function() {
  document.getElementById("loading").style.display = "none";
});

// Loading Animation at Home Page after Clicking Submit Button
window.onload = function() {
  document.querySelector(".loading").classList.remove("show-loading");
};

window.onbeforeunload = function() {
  document.querySelector(".loading").classList.add("show-loading");
};



// Read More Pannel Opening After Clicking Read More
document.getElementById("readMore").addEventListener("click", function () {
  document.getElementById("myModal").style.display = "block";
});

document.getElementById("close").addEventListener("click", function () {
  document.getElementById("myModal").style.display = "none";
});

window.addEventListener("click", function (event) {
  if (event.target == document.getElementById("myModal")) {
    document.getElementById("myModal").style.display = "none";
  }
});




// hjkahsssssss








 

  