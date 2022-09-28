import "url-search-params-polyfill";
import "fetch-polyfill";
import { progressivelyEnhanceMultipleSelectField } from "core/multi-select";

export default function initAddGood() {
  var plural = [];

  $("#unit > option").each(function () {
    if ($(this).text().endsWith("(s)")) {
      plural.push($(this).val());
    }
  });

  for (var i = 0; i < plural.length; i++) {
    key = plural[i];
    option = $("#unit > option[value=" + key + "]");
    option.text(option.text().substring(0, option.text().length - 3) + "s");
  }

  $("#quantity").on("input propertychange paste", function () {
    for (var i = 0; i < plural.length; i++) {
      key = plural[i];
      option = $("#unit > option[value=" + key + "]");
      if ($(this).val() == "1") {
        if (option.text().endsWith("s")) {
          option.text(option.text().substring(0, option.text().length - 1));
        }
      } else {
        if (!option.text().endsWith("s")) {
          option.text(option.text() + "s");
        }
      }
    }
  });

  function showHideCertificateMissingReason() {
    var textarea = $("#section_certificate_missing_reason");
    var label = $('label[for="section_certificate_missing_reason"]');

    if ($("input[name='section_certificate_missing']").is(":checked")) {
      label.show();
      textarea.show();
    } else {
      label.hide();
      textarea.hide();
    }
  }

  $("input[name='section_certificate_missing']").change(function () {
    showHideCertificateMissingReason();
  });

  function populateUploadedCertificate() {
    var existingCertificate = $("input[name='uploaded_file_name']").val();
    if (existingCertificate) {
      $("input[type=file]")
        .next()
        .html(
          existingCertificate +
            "<br><span class='lite-file-upload__or-label'>Drag and drop your document here or <span class='lite-file-upload__link'>click to browse</span> to replace it</span>"
        );
    }
  }

  (function () {
    populateUploadedCertificate();
    showHideCertificateMissingReason();
  })();

  (function () {
    var controlListEntriesField = document.getElementById(
      "control_list_entries"
    );
    if (!controlListEntriesField) {
      return;
    }

    var controlListEntriesTokenFieldInfo = document.createElement("div");
    controlListEntriesField.parentElement.appendChild(
      controlListEntriesTokenFieldInfo
    );

    progressivelyEnhanceMultipleSelectField(controlListEntriesField);
  })();
}
