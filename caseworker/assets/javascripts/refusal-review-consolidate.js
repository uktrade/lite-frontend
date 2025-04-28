import MultiSelector from "core/multi-selector";

const initDenialReasons = (elementId) => {
  const denialReasonField = document.getElementById(elementId);
  if (!denialReasonField) return;
  const multiSelector = new MultiSelector(denialReasonField);
  multiSelector.init();
};

initDenialReasons("id_denial_reasons");
initDenialReasons("id_release_request_refusal_reasons-refusal_reasons");
