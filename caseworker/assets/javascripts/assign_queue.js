var message =
  "This case has a next review date set in the future. If you are the last person in your team " +
  "assigned to this case, this action will clear the next review date. Are you sure you would like to submit?";

$("#button-Submit").click(function () {
  return confirm(message);
});

$("#button-done").click(function () {
  return confirm(message);
});
