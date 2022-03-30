(function () {
  function updateTotalValue() {
    var valuePerItem =
      this.getAttribute("data-applied-for-value") /
      this.getAttribute("data-applied-for-quantity");
    var outputElement = document.getElementById(
      this.getAttribute("data-output-element-id")
    );
    outputElement.value = (this.value * valuePerItem).toFixed(2);
  }
  var elements = document.getElementsByClassName("js-update-total-value");
  for (var i = 0; i < elements.length; i++) {
    elements.item(i).addEventListener("keyup", updateTotalValue);
  }
})();
