$.fn.changeElementType = function (newType) {
  var attrs = {};

  $.each(this[0].attributes, function (idx, attr) {
    attrs[attr.nodeName] = attr.nodeValue;
  });

  var newelement = $("<" + newType + "/>", attrs).append($(this).contents());
  this.replaceWith(newelement);
  return newelement;
};

$("[data-max-length]").each(function () {
  var originalText = $(this).html();
  var shrunkText = $(this).html().substring(0, $(this).data("max-length"));

  if (originalText.length != shrunkText.length) {
    $(this).html(shrunkText + "...");
    var $more = $(
      "<a href='#' class='govuk-link govuk-link--no-visited-state govuk-!-margin-left-2'>More</a>"
    ).appendTo($(this));
    $more.attr("data-more-text", originalText);
  }
});

$("[data-more-text]").click(function () {
  $(this).parent().html($(this).data("more-text"));
  return false;
});

$("[data-definition-title]").each(function () {
  $(this).addClass("lite-link--definition");
  $(this).changeElementType("a").attr("href", "#");
});

$("[data-definition-title]").click(function () {
  var subtitle = $(this).data("definition-subtitle");
  var text = $(this).data("definition-text");
  var list = $(this).data("definition-list");
  if (list) {
    list = list.split(",");
  }
  var htmlList = "<ol class='govuk-list govuk-list--number'>";

  if (list) {
    for (var i = 0; i < list.length; i++) {
      htmlList += "<li>" + list[i] + "</li>";
    }
  }

  htmlList = htmlList + "</ol>";

  if (subtitle) {
    subtitle = "<p class='govuk-heading-s'>" + subtitle + "</p>";
    if (text) {
      text = subtitle + text;
    } else {
      htmlList = subtitle + htmlList;
    }
  }

  LITECommon.Modal.showModal(
    $(this).data("definition-title"),
    text || htmlList,
    false,
    true,
    { maxWidth: "500px" }
  );
  return false;
});
