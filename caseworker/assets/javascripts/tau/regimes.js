import { progressivelyEnhanceMultipleSelectField } from "core/multi-select";

const initRegimes = () => {
  const regimeSelects = document.querySelectorAll(
    "[data-module=regimes-multi-select]"
  );

  for (let regimeSelect of regimeSelects) {
    progressivelyEnhanceMultipleSelectField(regimeSelect, (option) => {
      return { id: option.value, name: option.label, classes: [] };
    });
  }
};

export default initRegimes;
