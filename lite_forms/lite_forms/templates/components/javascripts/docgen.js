function showFlagsModal() {
    LITECommon.Modal.showModal("Formatting", $("#flags-modal").html(), false);
    return false;
}

var currentMousePos = { x: -1, y: -1 };
$(document).mousemove(function(event) {
    currentMousePos.x = event.pageX;
    currentMousePos.y = event.pageY;
});

$('textarea').mouseup(function() {
    var text=getSel();
    if (text.length == 0) {
        $(".app-document-formatter").fadeOut(100);
    } else {
        $(".app-document-formatter").fadeIn(100);
        $(".app-document-formatter").css({'top': currentMousePos.y, 'left': currentMousePos.x})
    }
});

$.fn.selectRange = function(start, end) {
    var e = document.getElementById($(this).attr('id')); // I don't know why... but $(this) don't want to work today :-/
    if (!e) return;
    else if (e.setSelectionRange) { e.focus(); e.setSelectionRange(start, end); } /* WebKit */
    else if (e.createTextRange) { var range = e.createTextRange(); range.collapse(true); range.moveEnd('character', end); range.moveStart('character', start); range.select(); } /* IE */
    else if (e.selectionStart) { e.selectionStart = start; e.selectionEnd = end; }
};

function boldText() {
    var editor = document.getElementById("content");
    var editorHTML = editor.value;
    var selectionStart = 0, selectionEnd = 0;
    if (editor.selectionStart) selectionStart = editor.selectionStart;
    if (editor.selectionEnd) selectionEnd = editor.selectionEnd;
    if (selectionStart != selectionEnd) {
        var editorCharArray = editorHTML.split("");
        editorCharArray.splice(selectionEnd, 0, "**");
        editorCharArray.splice(selectionStart, 0, "**"); //must do End first
        editorHTML = editorCharArray.join("");
        editor.value = editorHTML;
    }
    $('#content').selectRange(selectionStart, selectionEnd + 4);
    $('#content').highlightWithinTextarea('update');
}

function italicText() {
    var editor = document.getElementById("content");
    var editorHTML = editor.value;
    var selectionStart = 0, selectionEnd = 0;
    if (editor.selectionStart) selectionStart = editor.selectionStart;
    if (editor.selectionEnd) selectionEnd = editor.selectionEnd;
    if (selectionStart != selectionEnd) {
        var editorCharArray = editorHTML.split("");
        editorCharArray.splice(selectionEnd, 0, "_");
        editorCharArray.splice(selectionStart, 0, "_"); //must do End first
        editorHTML = editorCharArray.join("");
        editor.value = editorHTML;
    }
    $('#content').selectRange(selectionStart, selectionEnd + 2);
    $('#content').highlightWithinTextarea('update');
}

function getSel() {
    // obtain the object reference for the <textarea>
    var txtarea = document.getElementById("content");
    // obtain the index of the first selected character
    var start = txtarea.selectionStart;
    // obtain the index of the last selected character
    var finish = txtarea.selectionEnd;
    // obtain the selected text
    var sel = txtarea.value.substring(start, finish);
    // do something with the selected content
    return sel;
}
