function enableButton(button) {
  $(button)
    .prop("disabled", false)
    .removeClass("govuk-button--disabled")
    .attr("aria-disabled", false);
}

function disableButton(button) {
  $(button)
    .prop("disabled", true)
    .addClass("govuk-button--disabled")
    .attr("aria-disabled", true);
}

function enableLink(link) {
  $(link)
    .prop("disabled", false)
    .removeClass("govuk-link--disabled")
    .attr("aria-disabled", false)
    .removeAttr("tabindex");
}

function disableLink(link) {
  $(link)
    .prop("disabled", true)
    .addClass("govuk-link--disabled")
    .attr("aria-disabled", true)
    .attr("tabindex", "-1");
}

export { enableButton, disableButton, enableLink, disableLink };
