const MIN_LENGTH = 1;
const VISIBLE_LENGTH = 1000;
const MAX_LENGTH = 2200;

$("#response").on("input propertychange paste", function () {
  if ($(this).val().length > VISIBLE_LENGTH) {
    $("#response-length-warning").text(
      "You have " +
        (MAX_LENGTH - $(this).val().length) +
        " character" +
        pluralize(MAX_LENGTH - $(this).val().length) +
        " remaining"
    );
  } else {
    $("#response-length-warning").text(
      "You can enter up to " + MAX_LENGTH + " characters"
    );
  }

  if ($(this).val().length > MAX_LENGTH) {
    $("#response-length-warning").text(
      "You have " +
        ($(this).val().length - MAX_LENGTH) +
        " character" +
        pluralize($(this).val().length - MAX_LENGTH) +
        " too many"
    );
    $("#response-text-container").addClass("govuk-form-group--error");
  } else {
    $("#response-text-container").removeClass("govuk-form-group--error");
  }
});
