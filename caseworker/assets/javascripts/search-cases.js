(function() {
  var inputElement = document.getElementById("id_search_string")
  var searchButtonElement = document.getElementById('search-button')
  var resultsElement = document.getElementById("results-table")
  var currentSearch = inputElement.value || ''
  var lastSearch = inputElement.value || ''
  var datePicker = null

  // focus at end of the field and make sure there is a space at the end
  inputElement.focus()
  if (!/ $/.test(inputElement.value)) {
    inputElement.value = inputElement.value + ' '
  }
  inputElement.setSelectionRange(inputElement.value.length,inputElement.value.length)

  var autocomplete = new autoComplete({
    trigger: {
      event: ['input'],
      condition: function(query) {
        if (isCalendarIntent(query)) {
          return false
        } else {
          return query.length > autocomplete.threshold && query !== " "
        }
      }
    },
    data: {
      src: function() {
        currentSearch = inputElement.value.replace(lastSearch, '').trim()
        var query = currentSearch.toLowerCase()
        return fetch('/search/suggest/?format=json&q=' + query).then(function(response) {
          return response.json().then(function(parsed) {
            // cheap prefix match "incor" for "spire"
            if (currentSearch.indexOf('spi') > -1) {
              parsed = [{'field': 'database', 'value': 'SPIRE'}].concat(parsed)
            // cheap prefix match "incor" for "lite"
            } else if (currentSearch.indexOf('lit') > -1 ) {
              parsed = [{'field': 'database', 'value': 'LITE'}].concat(parsed)
            // cheap prefix match "incor" for "incorporated"
            } else if (currentSearch.indexOf('incor') > -1) {
              parsed = [
                {'field': 'incorporated', 'value': 'true'},
                {'field': 'incorporated', 'value': 'false'},

              ].concat(parsed)
            }
            return parsed
          })
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
        var value = data.value.value.replace(/\s/g, " ")
        var prefix = ''
        if (data.value.field != 'wildcard') {
          prefix += '<td class="autoCompleteResultFieldName">' + data.value.field.replace(/_/g, ' ') + '</td>'
        }
        source.innerHTML = prefix + '<td>' + value + '</td>'
      },
      element: "tr"
    },
    searchEngine: function(query, record) {
        return record
    },
    maxResults: 5,
    onSelection: function(feedback) {
      if (feedback.selection.value.field == 'wildcard') {
        var appendValue = feedback.selection.value.value 
      } else {
        var appendValue = feedback.selection.value.field + ':"' + feedback.selection.value.value + '"'
      }
      inputElement.value = inputElement.value.replace(currentSearch, appendValue + ' ')
      handleSearch()
    }
  });

  function isCalendarIntent(query) {
    query = query.toLowerCase()
    return query.indexOf('created:') > -1 || query.indexOf('updated:') > -1
  }

  function handleSearch() {
    var query = lastSearch = inputElement.value
    setTimeout(function() { inputElement.focus()})
    fetch('/search/?search_string=' + query).then(function(response) {
      var html = response.text().then(function(html) {
        var div = document.createElement('div');
        div.innerHTML = html.trim();
        document.getElementsByClassName('results-area')[0].innerHTML = div.getElementsByClassName('results-area')[0].innerHTML
      })
    })
    var searchParams = new URLSearchParams(window.location.search);
    searchParams.set("search_string", query);
    history.pushState(null, '', window.location.pathname + '?' + searchParams.toString());
  }

  function handleDateInput(fieldName) {
    datePicker = new Lightpick({
      field: document.createElement('input'),
      inline: true,
      parentEl: inputElement.parentNode,
      singleDate: false,
      onSelect: function(start, end){
        var startField = fieldName + '__gte'
        var endField = fieldName + '__lte'
        if (start && end) {
          inputElement.value = inputElement.value.trim().replace(
            fieldName + ':',
            startField + ':"' + start.format('YYYY-MM-DD') + '" ' + endField + ':"' + end.format('YYYY-MM-DD') + '"'
          )
          handleSearch()
          this.destroy()
          datePicker = null;
        }
      }
    })
  }

  searchButtonElement.addEventListener('click', function(event) {
    event.preventDefault()
    handleSearch()
  })

  inputElement.addEventListener('keyup', function() {
    // only open date picker if not already open
    if (!datePicker && isCalendarIntent(this.value)) {
      var fieldName = this.value.indexOf('created:') > -1 ? 'created' : 'updated'
      handleDateInput(fieldName)
    }
  })

})()
