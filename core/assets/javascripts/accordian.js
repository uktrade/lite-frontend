$(".lite-accordian-table__chevron").click(function () {
  $(this)
    .parent()
    .parent()
    .find(".app-expanded-row__item, .app-expanded-row__item--invert")
    .toggle();
  $(this).parent().parent().toggleClass("open");
  return false;
});
