import MultiSelector from "core/multi-selector";

const initDenialReasons = () => {
  const denialReasonField = document.getElementById("id_denial_reasons");
  if (!denialReasonField) return;
  const multiSelector = new MultiSelector(denialReasonField);
  multiSelector.init();
};

initDenialReasons();
