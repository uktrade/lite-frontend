import MultiSelector from "core/multi-selector";

const initRegimes = () => {
  const regimeSelects = document.querySelectorAll(
    "[data-module=regimes-multi-select]"
  );

  for (const regimeSelect of regimeSelects) {
    const multiSelector = new MultiSelector(regimeSelect);
    multiSelector.init();
  }
};

export default initRegimes;
