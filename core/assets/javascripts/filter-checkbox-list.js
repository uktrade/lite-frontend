$(".lite-search__container").show();

$("#filter-box").on("input", function () {
  var value = $(this).val().toLowerCase();

  $(".govuk-checkboxes__item").each(function (i, obj) {
    var checkboxText = $(obj)
      .find(".govuk-checkboxes__label")
      .text()
      .toLowerCase();
    var checkboxDescription = $(obj)
      .find(".govuk-checkboxes__hint")
      .text()
      .toLowerCase();

    // Show checkbox if it's in the filter
    if (checkboxText.includes(value) || checkboxDescription.includes(value)) {
      $(obj).show();
      $(obj).addClass("visible");
    } else {
      $(obj).hide();
      $(obj).removeClass("visible");
    }
  });
});

var mark = function () {
  var keyword = $("#filter-box").val();

  // Remove previous marked elements and mark
  // the new keyword inside the context
  $(".govuk-checkboxes__label").unmark({
    done: function () {
      $(".govuk-checkboxes__label").mark(keyword, {
        className: "lite-highlight",
      });
    },
  });
};

$("#filter-box").on("input", mark);
