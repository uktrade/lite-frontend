let text_for = "text";
let text_label = $("label[for=" + text_for + "]");

$(document).ready(function () {
  text_label.append('<span class="lite-form-optional">(optional)</span>');
  addOrRemoveOptional();
});

$(".govuk-radios--conditional").on("click", function () {
  addOrRemoveOptional();
});

function addOrRemoveOptional() {
  let advice_decision = $('input:radio[id="type-refuse"]:checked').val();

  // if the advice decision isn't 'Refuse', add (optional) to the reason for decision title
  if (advice_decision !== "refuse" && !text_label.children().is("span")) {
    text_label.append('<span class="lite-form-optional">(optional)</span>');
  }

  if (advice_decision === "refuse") {
    text_label.children().remove();
  }
}
