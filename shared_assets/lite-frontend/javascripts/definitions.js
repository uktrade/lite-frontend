$.fn.changeElementType = function(newType) {
    var attrs = {};

    $.each(this[0].attributes, function(idx, attr) {
        attrs[attr.nodeName] = attr.nodeValue;
    });

    var newelement = $("<" + newType + "/>", attrs).append($(this).contents());
    this.replaceWith(newelement);
    return newelement;
};

$('[data-definition-title]').each(function() {
	$(this).addClass("lite-link--definition");
	$(this).changeElementType("a").attr("href", "#");
});

$('[data-definition-title]').click(function() {
    LITECommon.Modal.showModal($(this).data("definition-title"), $(this).data("definition-text"), false, true, {maxWidth: '500px'});
    return false;
})