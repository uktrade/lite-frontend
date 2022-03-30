$(".govuk-back-link").on("click", function () {
  var address = $(this).attr("href");
  if (address != "#") {
    window.location.href = address;
  } else {
    window.history.go(-1);
  }
  return false;
});
