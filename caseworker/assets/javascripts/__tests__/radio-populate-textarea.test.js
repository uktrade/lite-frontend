import { getByTestId } from "@testing-library/dom";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";
import { PopulateTextOnRadioInput } from "../radio-populate-textarea";
let radio_document;

const createRadioElement = () => {
  document.body.innerHTML = `
    <form>
        <div data-module="radio-textarea">
            <fieldset>
                <input type="radio" value="no_clear_concerns" />
                <input type="radio" value="no_concerns" />
                <input type="radio" value="refuse_licence_application" />
            </fieldset>
            <div id="div_id_approval_reasons">
                <textarea name="approval_reasons"></textarea>
            </div>
            <script id="approval_reasons" type="application/json">
                {
                    "no_clear_concerns": "No clear concerns text",
                    "no_concerns": "No Concerns Text",
                    "refuse_licence_application": "Refuse Licence Application TEXT"
                }
            </script>
        </div>
    </form>

    `;
  return document.querySelector("form");
};

describe("Radio Populate Textarea", () => {
  beforeEach(() => {
    radio_document = createRadioElement();
    new PopulateTextOnRadioInput(radio_document).init();
  });

  test("click radio button updates text area", async () => {
    let text_area = radio_document.querySelector("textarea");
    expect(text_area.value).toBe("");
    let radio_buttons = radio_document.querySelectorAll("input[type=radio]");
    await userEvent.click(radio_buttons[0]);
    expect(text_area.value).toBe("No clear concerns text");
  });

  test("keyboard navigation updates text area", async () => {
    let text_area = radio_document.querySelector("textarea");
    expect(text_area.value).toBe("");
    let radio_buttons = radio_document.querySelectorAll("input[type=radio]");
    // pressing tab doesn't select the item
    await userEvent.tab();
    expect(radio_buttons[0]).toHaveFocus();
    expect(text_area.value).toBe("");

    // space selects the first item
    await userEvent.keyboard("[Space]");
    expect(radio_buttons[0]).toHaveFocus();
    expect(text_area.value).toBe("No clear concerns text");

    // tab takes you to the next item and space selects it
    await userEvent.tab();
    await userEvent.keyboard("[Space]");
    expect(radio_buttons[1]).toHaveFocus();
    expect(text_area.value).toBe("No Concerns Text");
  });
});
