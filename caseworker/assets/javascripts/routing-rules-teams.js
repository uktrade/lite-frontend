$(document).ready(function () {
  var queues = [];

  // custom event triggered on autocomplete change. see lite_forms/templates/components/autocomplete.html
  document.addEventListener("autocomplete team change", function (e) {
    var teamID = e.detail;

    if (teamID) {
      fetch("/api/teams/" + teamID + "/queues/?disable_pagination=True").then(
        function (response) {
          return response.json().then(function (data) {
            var emptyOption = {
              id: null,
              name: "",
            };
            queues = [emptyOption].concat(data);
            // update the queue select's options with new options
            var $queuesSelect = $("#queue-select");
            $queuesSelect.attr("id", "queue");
            $queuesSelect.empty();

            queues.forEach((queue) => {
              var $option = $("<option></option>");
              $option.val(queue.id).text(queue.name);
              $queuesSelect.append($option);
            });

            $("#queue").remove();

            rerenderAutocomplete("queue");
          });
        }
      );
    }
  });

  function rerenderAutocomplete(name) {
    var selectElement = document.querySelector("select[name=" + name + "]");

    accessibleAutocomplete.enhanceSelectElement({
      defaultValue: "",
      displayMenu: "overlay",
      selectElement: selectElement,
      cssNamespace: "lite-autocomplete",
      onConfirm: (query) => {
        const requestedOption = [].filter.call(
          selectElement.options,
          (option) => (option.textContent || option.innerText) === query
        )[0];
        if (requestedOption) {
          requestedOption.selected = true;
          var changeEvent = new CustomEvent(
            "autocomplete " + name + " change",
            { detail: requestedOption.value }
          );
          document.dispatchEvent(changeEvent);
        }
      },
    });
  }
});
