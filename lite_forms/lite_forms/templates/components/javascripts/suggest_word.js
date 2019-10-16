function getSuggestion(string) {
    if (!string.trim()) {
        return '';
    }

    returnValue = ''

    for (var key in text) {
        if (key.toLowerCase().startsWith(string.toLowerCase())) {
            if (key.toLowerCase() != string.toLowerCase()) {
                if (returnValue == '') {
                    returnValue = key;
                }
            }
        }
    }

    return returnValue;
}

function clickSuggestion(string) {
    replaceCurrentWord(string);
    $("#autocomplete-suggestions").empty();
}

function getSuggestions(string) {
    if (!string.trim()) {
        return [];
    }
    returnValue = [];

    for (var key in text) {
        if (key.toLowerCase().startsWith(string.toLowerCase())) {
            if (key.toLowerCase() != string.toLowerCase()) {
                returnValue.push([key, text[key]])
            }
        }
    }
    return returnValue;
}

function getCurrentWord() {
    var input = $("#content");
    var currentWord = '';
    var selectionStart = input.prop('selectionStart');
    var wordStart = input.val().substring(0, selectionStart).lastIndexOf(' ') + 1;
    currentWord = input.val().substring(wordStart, selectionStart);

    if (input.val().substring(0, selectionStart).lastIndexOf('{{') <= input.val().substring(0, selectionStart).lastIndexOf('}}') &&
        input.val().substring(0, selectionStart).lastIndexOf('{%') <= input.val().substring(0, selectionStart).lastIndexOf('%}')) {
        return '';
    }

    return currentWord;
}

function replaceCurrentWord(newWord) {
    var input = $("#content");
    var currentWord = '';
    var selectionStart = input.prop('selectionStart');
    var wordStart = input.val().substring(0, selectionStart).lastIndexOf(' ') + 1;

    input.val(input.val().replaceBetween(wordStart, selectionStart, newWord));

    $('#content').selectRange(wordStart + newWord.length, wordStart + newWord.length);

    $('#content').highlightWithinTextarea('update');
}
