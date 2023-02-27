$(".govuk-back-link:not(.govuk-back-link-nojs)").on("click", function () {
  var address = $(this).attr("href");
  if (address != "#") {
    window.location.href = address;
  } else {
    window.history.go(-1);
  }
  return false;
});
