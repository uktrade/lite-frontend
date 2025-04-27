import MultiSelector from "core/multi-selector";

const initDenialReasons = (element_id) => {
  const denialReasonField = document.getElementById(element_id);
  if (!denialReasonField) return;
  const multiSelector = new MultiSelector(denialReasonField);
  multiSelector.init();
};

initDenialReasons("id_denial_reasons");
initDenialReasons("id_release_request_refusal_reasons-refusal_reasons");
