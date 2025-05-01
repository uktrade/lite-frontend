import MultiSelector from "core/multi-selector";

const initDenialReasons = (className) => {
  const denialReasonFields = document.getElementsByClassName(className);
  if (denialReasonFields.length == 0) return;

  for (let field of denialReasonFields) {
    const multiSelector = new MultiSelector(field);
    multiSelector.init();
  }
};

initDenialReasons("lite-refusal-reasons-autocomplete");
