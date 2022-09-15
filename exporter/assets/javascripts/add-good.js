import "url-search-params-polyfill";
import "fetch-polyfill";
import Tokenfield from "./lite-tokenfield.js";

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

    function progressivelyEnhanceMultipleSelectField(element) {
      element.parentElement.classList.add("tokenfield-container");

      var items = [];
      var selected = [];
      for (var i = 0; i < element.options.length; i++) {
        var option = element.options.item(i);
        var item = { id: option.value, name: option.value, classes: [] };
        if (option.selected) {
          selected.push(item);
        }
        items.push(item);
      }
      var tokenField = new Tokenfield({
        el: element,
        items: items,
        newItems: false,
        addItemOnBlur: true,
        filterSetItems: false,
        addItemsOnPaste: true,
        minChars: 1,
        itemName: element.name,
        setItems: selected,
        keepItemsOrder: false,
      });
      tokenField._renderItems();
      tokenField._html.container.id = element.id;
      element.remove();
      return tokenField;
    }
  })();
}
