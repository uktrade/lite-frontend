let team = $("#team");

function filterDefaultQueueOptions(team_value, change_to_select) {
  // Only show queues that are owned by the selected team
  let default_queue = $("#default_queue");
  default_queue.children("option[data-attribute!='None']").hide();
  default_queue
    .children("option[data-attribute='" + team_value + "'], option[value='']")
    .show();

  // Set the selected value to 'Select'
  if (change_to_select === true) {
    default_queue.val("");
  }
}

team.change(function () {
  filterDefaultQueueOptions(team.val(), true);
});

team.ready(function () {
  filterDefaultQueueOptions(team.val(), false);
});
