import { progressivelyEnhanceMultipleSelectField } from "core/multi-select.js";

const initDenialReasons = () => {
  const denialReasonField = document.getElementById("id_denial_reasons");
  if (!denialReasonField) return;

  progressivelyEnhanceMultipleSelectField(denialReasonField);
};

initDenialReasons();
