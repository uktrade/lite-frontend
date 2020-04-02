function openTableFold(element) {
	$(element).parent().parent().find(".app-expanded-row__item, .app-expanded-row__item--invert").toggle();
	$(element).parent().parent().toggleClass("open");
	return false;
}
