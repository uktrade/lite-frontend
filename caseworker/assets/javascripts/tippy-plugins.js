const hideOnEsc = {
  name: "hideOnEsc",
  defaultValue: true,
  fn({ hide }) {
    function onKeyDown(event) {
      if (event.keyCode === 27) {
        hide();
      }
    }

    return {
      onShow() {
        document.addEventListener("keydown", onKeyDown);
      },
      onHide() {
        document.removeEventListener("keydown", onKeyDown);
      },
    };
  },
};

const makeFocusable = {
  name: "makeFocusable",
  defaultValue: true,
  fn() {
    return {
      onCreate: (instance) => {
        const element = instance.reference;
        element.setAttribute("tabindex", 0);
      },
    };
  },
};

export { hideOnEsc, makeFocusable };
