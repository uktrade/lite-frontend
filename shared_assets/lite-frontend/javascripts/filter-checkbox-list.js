$(".lite-search-wrapper").show();

$("#filter-box").on('input', function() {
	var value = $(this).val().toLowerCase();

	$(".govuk-checkboxes__item").each(function(i, obj) {
		var checkboxText = $(obj).find(".govuk-checkboxes__label").text().toLowerCase();
		var checkboxDescription = $(obj).find(".govuk-checkboxes__hint").text().toLowerCase();

		// Show checkbox if it's in the filter
	    if (checkboxText.includes(value) || checkboxDescription.includes(value)) {
			$(obj).show();
		} else {
			$(obj).hide();
		}
	});
});

$("input[type='checkbox']").change(function() {
	var checkboxText = $(this).parent().find(".govuk-checkboxes__label").text();
	addCheckedCheckboxesToList();
});

$(".govuk-grid-column-one-third").addClass("lite-related-items--sticky");
$(".govuk-grid-column-one-third").append("<div id='checkbox-counter' class='lite-related-items'>" +
											"<h2 id='checkbox-list-title' class='govuk-heading-m'>0 Selected</h2>" +
											"<div id='checkbox-list'></div>" +
										 "</div>");

function addCheckedCheckboxesToList() {
	$("#checkbox-list").empty();
	$("#checkbox-list-title").text($("input[type='checkbox']:checked").length + " Selected");
	$("input[type='checkbox']:checked").each(function(i, obj) {
		var checkboxText = $(this).parent().find(".govuk-checkboxes__label").text();
		$("#checkbox-list").append("<div><a class='govuk-link lite-checkbox-filter-link' href='#" + checkboxText.trim() + "'>" + checkboxText + "</a></div>");
	});
	if ($("input[type='checkbox']:checked").length == 0) {
		$("#checkbox-counter").hide();
	} else {
		$("#checkbox-counter").show();
	}

	$("a").on('click', function(event) {
		// Make sure this.hash has a value before overriding default behavior
		if (this.hash !== "") {
			// Prevent default anchor click behavior
			event.preventDefault();

			// Store hash
			var hash = this.hash.substr(1);

			console.log(hash);

			// Using jQuery's animate() method to add smooth page scroll
			// The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
			$('html, body').animate({
				scrollTop: $('[id="' + hash + '"]').offset().top
			}, 400, function() {

				// Add hash (#) to URL when done scrolling (default click behavior)
				window.location.hash = hash;
			});
		} // End if
	});
}

addCheckedCheckboxesToList();
