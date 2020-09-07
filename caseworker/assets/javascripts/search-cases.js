(function() {
  var lastSearch = ''
  var currentSearch = ''
  var element = document.getElementById("id_search_string")
  var resultsElement = document.getElementById("results-table")
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
    threshold: 0,
    debounce: 300,
    resultsList: {
      render: true,
      element: 'table'
    },
    resultItem: {
        content: function(data, source) {
            if (data.value.field == 'wildcard') {
                source.innerHTML = '<td>' + data.value.value + '</td>'
            } else {
                source.innerHTML = '<td class="autoCompleteResultFieldName">' + data.value.field + '</td><td>' + data.value.value + '<td/>'
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
      lastSearch = element.value = element.value.replace(currentSearch, appendValue + ' ')
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