var title = document.title;

var titleMap = {
  rejected: "All rejected LITE organisations",
  "in review": "All in review LITE organisations",
  active: "All active LITE organisations",
};

var setTitle = function () {
  var title_heading = document
    .getElementsByClassName("lite-tabs__tab--selected")[0]
    .text.trim()
    .toLowerCase();
  document.title = `${titleMap[title_heading]}`;
};
var elements = document.getElementsByClassName("lite-tabs__tab");

for (var i = 0; i < elements.length; i++) {
  elements[i].addEventListener("click", setTitle, false);
}
setTitle();
