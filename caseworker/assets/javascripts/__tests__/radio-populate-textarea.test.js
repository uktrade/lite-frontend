import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";
import { PopulateTextOnRadioInput } from "../radio-populate-textarea";
let radioDocument;

const createRadioElement = () => {
  document.body.innerHTML = `
    <form>
        <fieldset data-module="radio-textarea">
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
        </fieldset>
    </form>

    `;
  return document.querySelector("form");
};

describe("Radio Populate Textarea", () => {
  beforeEach(() => {
    radioDocument = createRadioElement();
    new PopulateTextOnRadioInput(radioDocument).init();
  });

  test("click radio button updates text area", async () => {
    let textArea = radioDocument.querySelector("textarea");
    expect(textArea.value).toBe("");
    let radioButtons = radioDocument.querySelectorAll("input[type=radio]");
    await userEvent.click(radioButtons[0]);
    expect(textArea.value).toBe("No clear concerns text");
  });

  test("keyboard navigation updates text area", async () => {
    let textArea = radioDocument.querySelector("textarea");
    expect(textArea.value).toBe("");
    let radioButtons = radioDocument.querySelectorAll("input[type=radio]");
    // pressing tab doesn't select the item
    await userEvent.tab();
    expect(radioButtons[0]).toHaveFocus();
    expect(textArea.value).toBe("");

    // space selects the first item
    await userEvent.keyboard("[Space]");
    expect(radioButtons[0]).toHaveFocus();
    expect(textArea.value).toBe("No clear concerns text");

    // tab takes you to the next item and space selects it
    await userEvent.tab();
    await userEvent.keyboard("[Space]");
    expect(radioButtons[1]).toHaveFocus();
    expect(textArea.value).toBe("No Concerns Text");
  });
});
