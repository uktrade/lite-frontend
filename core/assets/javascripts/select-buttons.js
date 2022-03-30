$("input:checkbox").change(function () {
  setSelectButtonsState();
});

$(".lite-button-checkbox").click(function () {
  const $table = $(this).closest("table");

  if (
    $table.find("input:checkbox:checked").length ==
    $table.find("input:checkbox").length
  ) {
    $table.find("input:checkbox").prop("checked", false).change();
  } else {
    $table.find("input:checkbox").prop("checked", true).change();
  }

  setSelectButtonsState();
});

function setSelectButtonsState() {
  $("table").each(function (i, obj) {
    $(obj).find(".lite-button-checkbox").attr("class", "lite-button-checkbox");

    if (
      $(obj).find("input:checkbox:checked").length ==
      $(obj).find("input:checkbox").length
    ) {
      $(obj)
        .find(".lite-button-checkbox")
        .addClass("lite-button-checkbox--checked");
    } else if ($(obj).find("input:checkbox:checked").length != 0) {
      $(obj)
        .find(".lite-button-checkbox")
        .addClass("lite-button-checkbox--indeterminate");
    }

    // Force Webkit to repaint the button
    // DON'T REMOVE!
    $(obj).find(".lite-button-checkbox").css("display", "none").height();
    $(obj).find(".lite-button-checkbox").css("display", "block");
  });
}
