import "url-search-params-polyfill";
import "fetch-polyfill";

export default function initAddGood() {
  let plural = [];

  $("#unit > option").each(function () {
    if ($(this).text().endsWith("(s)")) {
      plural.push($(this).val());
    }
  });

  for (let i = 0; i < plural.length; i++) {
    let key = plural[i];
    let option = $("#unit > option[value=" + key + "]");
    option.text(option.text().substring(0, option.text().length - 3) + "s");
  }

  $("#quantity").on("input propertychange paste", function () {
    for (let i = 0; i < plural.length; i++) {
      let key = plural[i];
      let option = $("#unit > option[value=" + key + "]");
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
    let textarea = $("#section_certificate_missing_reason");
    let label = $('label[for="section_certificate_missing_reason"]');

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

  (function () {
    showHideCertificateMissingReason();
  })();
}
