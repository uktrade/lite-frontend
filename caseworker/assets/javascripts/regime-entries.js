import { progressivelyEnhanceMultipleSelectField } from "core/multi-select";

export default function initRegimeEntries() {
  const regimeEntriesField = document.getElementById(
    "regime_entries"
  );

  if (!regimeEntriesField) return;

  const regimeEntriesTokenField = progressivelyEnhanceMultipleSelectField(
    regimeEntriesField
  );
}
