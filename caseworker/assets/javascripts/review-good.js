(function() {
  var inputElementId = "report_summary"
  var inputElement = document.getElementById(inputElementId)
  new autoComplete({
    trigger: {
      event: ['input'],
    },
    data: {
      src: function() {
        var query = inputElement.value.toLowerCase()
        return fetch('/team/picklists/.json?type=report_summary&name=' + query).then(function(response) {
          return response.json().then(function(parsed) {
            return parsed.results.map(function(item) { return { 'value': item['name'], 'text': item['text'] }})
          })
        })
      },
      key: ["value"],
      cache: false
    },
    selector: "#" + inputElementId,
    threshold: 1,
    debounce: 300,
    resultsList: {
      render: true,
      element: 'table',
      // when version 8 is released we can remove this: https://github.com/TarekRaafat/autoComplete.js/issues/105
      container: source => {
        source.setAttribute('id', 'autoComplete_list');
        inputElement.addEventListener('autoComplete', function (event) {
          function hideSearchResults() {
            var searchResults = document.getElementById('autoComplete_list');
            while (searchResults.firstChild) {
                searchResults.removeChild(searchResults.firstChild);
            }
            document.removeEventListener('click', hideSearchResults);
          }
          document.addEventListener('click', hideSearchResults);
        })
      },
    },
    resultItem: {
      content: function(data, source) {
        source.innerHTML = (
            '<td>' +
                '<div class="govuk-heading-s govuk-!-margin-0">' + data.value.value + '</div>' +
                '<div class="govuk-caption-xs govuk-!-margin-0">' + data.value.text + '</div>' +
            '</td>'
        )
      },
      element: "tr"
    },
    searchEngine: function(query, record) {
        return record
    },
    onSelection: feedback => {
        inputElement.value = feedback.selection.value.text
    },
    maxResults: 15
  });

  var controlListEntriesField = document.getElementById('control_list_entries')
  var controlRationgField = document.getElementById('control_rating')

  controlRationgField.style.display = 'none';

  progressivelyEnhanceMultipleSelectField(controlListEntriesField)
  progressivelyEnhanceMultipleSelectField(controlRationgField)

  function progressivelyEnhanceMultipleSelectField(element) {
    element.parentElement.classList.add('tokenfield-container')
    var items = []
    var selected = []
    for (var i = 0; i < element.options.length; i++) {
      var option = element.options.item(i)
      var item = {'id': option.value, 'name': option.value, 'classes': []}
      if (option.selected) {
          selected.push(item)
      }
      items.push(item)
    }
    var tokenField = new Tokenfield({
      el: element,
      items: items,
      newItems: false,
      addItemOnBlur: true,
      filterSetItems: false,
      addItemsOnPaste: true,
      minChars: 1,
      itemName: element.name,
      setItems: selected
    });

    tokenField._renderItem = function() {
      // the library appends '[]' to the end, django does not like that, so remove it here
      var itemHtml = Tokenfield.prototype._renderItem.apply(this, arguments)
      const input = itemHtml.querySelector('.item-input');
      input.setAttribute('name', input.name.replace('[]', ''));
      return itemHtml
    }
    tokenField._renderItems()
    element.remove()
  }
})()
