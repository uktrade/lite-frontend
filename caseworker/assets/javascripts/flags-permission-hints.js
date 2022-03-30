$("input[type='checkbox']").change(function () {
  if ($(this).attr("data-attribute") == "cannot-remove") {
    var id = $(this).val() + "-permission-hint";
    var $hint = $(
      "<span>You do not have permission to remove this flag once it is added.</span>"
    );
    $hint.attr({ id: id });

    if ($(this).is(":checked")) {
      if ($("#" + id).length == 0) {
        $(this).parent().append($hint);
      }
    } else {
      $("#" + id).remove();
    }
  }
});
