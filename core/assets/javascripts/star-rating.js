const initStarRating = () => {
  const radios = document.querySelectorAll("#star_rating input[type=radio]");
  let output = document.querySelector("#star_rating #output");

  Array.prototype.forEach.call(radios, function (el) {
    let label = el.nextSibling.nextSibling;
    label.addEventListener("click", function () {
      output.textContent = label.querySelector("span").textContent;
    });
  });
};

export default initStarRating;
