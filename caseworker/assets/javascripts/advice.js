/* global $ */

let textFor = "text";
let textLabel = $("label[for=" + textFor + "]");

$(document).ready(function () {
  textLabel.append('<span class="lite-form-optional">(optional)</span>');
  addOrRemoveOptional();
});

$(".govuk-radios--conditional").on("click", function () {
  addOrRemoveOptional();
});

function addOrRemoveOptional() {
  let adviceDecision = $('input:radio[id="type-refuse"]:checked').val();

  // if the advice decision isn't 'Refuse', add (optional) to the reason for decision title
  if (adviceDecision !== "refuse" && !textLabel.children().is("span")) {
    textLabel.append('<span class="lite-form-optional">(optional)</span>');
  }

  if (adviceDecision === "refuse") {
    textLabel.children().remove();
  }
}
