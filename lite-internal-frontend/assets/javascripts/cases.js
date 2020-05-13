function openTableFold(element) {
	$(element).parent().parent().find(".app-expanded-row__item, .app-expanded-row__item--invert").toggle();
	$(element).toggleClass("lite-expand__control--open");
	updateTableFoldControl();
	return false;
}

function updateTableFoldControl() {
	if ($(".lite-expand__control").length == $(".lite-expand__control--open").length) {
		$("#link-open-all-table-folds").addClass("lite-expand__base-control--open");
	} else {
		$("#link-open-all-table-folds").removeClass("lite-expand__base-control--open");
	}
}

function toggleTableFold() {
	if ($(".lite-expand__control").length == $(".lite-expand__control--open").length) {
		$(".app-expanded-row__item").hide();
		$(".app-expanded-row__item--invert").show();
		$(".lite-expand__control").removeClass("lite-expand__control--open");
	} else {
		$(".app-expanded-row__item").show();
		$(".app-expanded-row__item--invert").hide();
		$(".lite-expand__control").addClass("lite-expand__control--open");
	}

	updateTableFoldControl();

	return false;
}
