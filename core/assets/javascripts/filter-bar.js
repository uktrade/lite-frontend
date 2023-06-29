function tryShowFilterBar() {
  $(".lite-filter-bar").each(function () {
    var $filters = $(this).parent();
    $filters.hide();
    $filters.prev().find("#show-filters-link").show();
    $filters.prev().find("#hide-filters-link").hide();

    $(this)
      .find("input, select")
      .each(function () {
        if (
          $(this).val() != "" &&
          $(this).val() != "Select" &&
          $(this).val() != "blank" &&
          $(this).attr("type") != "hidden" &&
          ($(this).attr("type") != "checkbox" ||
            ($(this).attr("type") == "checkbox" && $(this).attr("checked")))
        ) {
          $filters.show();
          $filters.prev().find("#show-filters-link").hide();
          $filters.prev().find("#hide-filters-link").show();
          $(this).parents(".govuk-details").attr("open", "");
        }
      });
  });
}

tryShowFilterBar();

$(".lite-filter-toggle-link")
  .unbind()
  .click(function () {
    var $filters = $(this).parent().next();
    $filters.toggle();
    $(this).parent().find("> *").toggle();

    return false;
  });
