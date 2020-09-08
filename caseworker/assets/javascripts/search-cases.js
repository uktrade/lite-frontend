(function() {
  var element = document.getElementById("id_search_string")
  var resultsElement = document.getElementById("results-table")
  var currentSearch = element.value || ''
  var lastSearch = element.value || ''

  // focus at end of the field
  element.focus()
  element.setSelectionRange(element.value.length,element.value.length)

  new autoComplete({
    data: {
      src: function() {
        query = currentSearch = element.value.replace(lastSearch, '')
        return fetch('/search/suggest/?format=json&q=' + query).then(function(response) {
            return response.json()
        })
      },
      key: ["value"],
      cache: false
    },
    selector: "#id_search_string",
    threshold: 1,
    debounce: 300,
    resultsList: {
      render: true,
      element: 'table',
      // when version 8 is released we can remove this: https://github.com/TarekRaafat/autoComplete.js/issues/105
      container: source => {
          source.setAttribute('id', 'autoComplete_list');
          document.getElementById('id_search_string').addEventListener('autoComplete', function (event) {
              function hideSearchResults() {
                  const searchResults = document.getElementById('autoComplete_list');
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
            if (data.value.field == 'wildcard') {
                source.innerHTML = '<td>' + data.value.value + '</td>'
            } else {
                source.innerHTML = '<td class="autoCompleteResultFieldName">' + data.value.field.replace('_', ' ') + '</td><td>' + data.value.value + '<td/>'
            }
        },
        element: "tr"
    },
    searchEngine: function(query, record) {
        return record
    },
    maxResults: 5,                         // Max. number of rendered results | (Optional)
    onSelection: function(feedback) {
      if (feedback.selection.value.field == 'wildcard') {
        var appendValue = feedback.selection.value.value 
      } else {
        var appendValue = feedback.selection.value.field + ':"' + feedback.selection.value.value + '"'
      }
      lastSearch = element.value = element.value.replace(currentSearch, ' ' + appendValue + ' ').replace('  ', ' ')
      setTimeout(function() { element.focus()})

      fetch('/search/?search_string=' + lastSearch).then(function(response) {
        var html = response.text().then(function(html) {
          var div = document.createElement('div');
          div.innerHTML = html.trim();
          document.getElementsByClassName('results-area')[0].innerHTML = div.getElementsByClassName('results-area')[0].innerHTML
        })
      })
      var searchParams = new URLSearchParams(window.location.search);
      searchParams.set("search_string", lastSearch);
      history.pushState(null, '', window.location.pathname + '?' + searchParams.toString());
    }
  });
})()
