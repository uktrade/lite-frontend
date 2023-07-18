import "@testing-library/jest-dom";
import PopulateTextOnRadioInput from "../radio-populate-textarea";
let radio_document;

const createRadioElement = () => {
  document.body.innerHTML = `
    <form data-module="refusals" method="post">
        <div id="div_id_refusal_picks" class="govuk-form-group">
            <fieldset class="govuk-fieldset">
                <legend class="govuk-fieldset__legend">
                    What is your reason for approving?
                </legend>
                <div class="govuk-radios">
                    <div class="govuk-radios__item">
                        <input type="radio" name="refusal_picks" value="no_concerns" />
                        <label> No concerns </label>
                    </div>
                    <div class="govuk-radios__item">
                        <input type="radio" name="refusal_picks" value="concerns" />
                        <label> Concerns </label>
                    </div>
                    <div class="govuk-radios__item">
                        <input
                            type="radio"
                            name="refusal_picks"
                            value="military_concerns"
                        />
                        <label> Military concerns </label>
                    </div>
                    <div class="govuk-radios__item">
                        <input type="radio" name="refusal_picks" value="wmd" />
                        <label> Weapons of mass destruction (WMD) concerns </label>
                    </div>
                    <div class="govuk-radios__item">
                        <input type="radio" name="refusal_picks" value="other" />
                        <label> Other </label>
                    </div>
                </div>
            </fieldset>
        </div>
        <div id="div_id_refusal_reasons" class="govuk-form-group">
            <textarea id="id_refusal_reasons"></textarea>
        </div>
    </form>
    `;
  return document.querySelector("form");
};

describe("Review Consolidate", () => {
  beforeEach(() => {
    radio_document = createRadioElement();
    const refusals_text = {
      no_concerns: "No Concerns",
      concerns: "Concerns",
      military_concerns: "Military concerns",
      wmd: "Weapons of mass destruction (WMD) concerns",
      other: "",
    };
    return new PopulateTextOnRadioInput(
      "input[name=refusal_picks]",
      "#id_refusal_reasons",
      refusals_text
    );
  });

  test("click radio button updates text area", async () => {
    let text_area = radio_document.querySelector("#id_refusal_reasons");
    expect(text_area.value).toBe("");
    let radio_buttons = radio_document.querySelectorAll(
      "input[name=refusal_picks]"
    );
    await radio_buttons[0].click();
    expect(text_area.value).toBe("No Concerns");
  });
});
