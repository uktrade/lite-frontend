const MIN_LENGTH = 1;
const VISIBLE_LENGTH = 1200;
const MAX_LENGTH = 2200;

$("#input-case-note").on("input propertychange paste", function () {
  if ($(this).val().length > VISIBLE_LENGTH) {
    $("#input-case-note-warning").text(
      "You have " +
        (MAX_LENGTH - $(this).val().length) +
        " character" +
        pluralize(MAX_LENGTH - $(this).val().length) +
        " remaining"
    );
  } else {
    $("#input-case-note-warning").text(
      "You can enter up to " + MAX_LENGTH + " characters"
    );
  }

  if ($(this).val().length > MAX_LENGTH) {
    $("#input-case-note-warning").text(
      "You have " +
        ($(this).val().length - MAX_LENGTH) +
        " character" +
        pluralize($(this).val().length - MAX_LENGTH) +
        " too many"
    );
    $("#input-case-note").parent().addClass("lite-case-note__container--error");
  } else {
    $("#input-case-note")
      .parent()
      .removeClass("lite-case-note__container--error");
  }
});

$("#link-case-note-cancel").on("click", function () {
  $("#input-case-note").val("");
  $("#input-case-note").trigger("input");
  $("#input-case-note").focus();
  return false;
});
