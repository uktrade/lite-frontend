if (!$(".lite-search__container").is(":hidden")) {
  $(".lite-search__container").show();
}

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

$("input[type='checkbox']").change(function () {
  addCheckedCheckboxesToList();
});

$(".govuk-grid-column-one-third").addClass("lite-related-items--sticky");
$(".govuk-grid-column-one-third").append(
  "<div id='checkbox-counter' class='lite-related-items'>" +
    "<h2 id='checkbox-list-title' class='govuk-heading-m'>0 Selected !!</h2>" +
    "<div id='checkbox-list'></div>" +
    "</div>"
);

function addCheckedCheckboxesToList() {
  var formattedText = "";
  $("#checkbox-list").empty();
  $("#checkbox-list-title").text("Flags selected");
  $("input[type='checkbox']:checked").each(function () {
    formattedText += this.dataset.attribute;
  });
  $("#checkbox-list").append(
    "<ol class='govuk-list govuk-!-padding-left-4' style='list-style:decimal'>" +
      formattedText +
      "</ol>"
  );
  if ($("input[type='checkbox']:checked").length == 0) {
    $("#checkbox-counter").hide().children().hide();
  } else {
    $("#checkbox-counter").show().children().show();
  }

  $("a").on("click", function (event) {
    // Make sure this.hash has a value before overriding default behavior
    if (this.hash !== "") {
      // Prevent default anchor click behavior
      event.preventDefault();

      // Store hash
      var hash = this.hash.substr(1);

      // Using jQuery's animate() method to add smooth page scroll
      // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
      $("html, body").animate(
        {
          scrollTop: $('[id="' + hash + '"]').offset().top,
        },
        400,
        function () {
          // Add hash (#) to URL when done scrolling (default click behavior)
          window.location.hash = hash;
        }
      );
    } // End if
  });
}

addCheckedCheckboxesToList();

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
