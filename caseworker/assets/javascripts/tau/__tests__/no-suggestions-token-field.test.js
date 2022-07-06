import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import NoSuggestionsTokenField from "../no-suggestions-token-field";

let tokenFieldContainer,
  noCleCheckbox,
  mockTokenfield,
  tokenFieldInput,
  tokenFieldSet,
  tokenFieldSetList,
  component;

const createElements = () => {
  document.body.innerHTML = `
    <div>
      <div id="token-field-container">
        <input type="text" class="tokenfield-input" />
        <div class="tokenfield-set">
          <ul></ul>
        </div>
      </div>
      <input type="checkbox" name="no-cle" />
    </div>
  `;

  mockTokenfield = {
    emptyItems: jest.fn(),
  };

  tokenFieldContainer = document.querySelector("#token-field-container");
  tokenFieldContainer.tokenfield = mockTokenfield;
  noCleCheckbox = document.querySelector("[name=no-cle]");
  tokenFieldInput = document.querySelector(".tokenfield-input");
  tokenFieldSet = document.querySelector(".tokenfield-set");
  tokenFieldSetList = document.querySelector(".tokenfield-set ul");

  return [tokenFieldContainer, noCleCheckbox];
};

const createComponent = () => {
  createElements();
  component = new NoSuggestionsTokenField(
    "#token-field-container",
    noCleCheckbox
  );
  component.init();
  return component;
};

describe("No suggestions token field", () => {
  beforeEach(() => {
    createComponent();
  });

  test("Checking no cle checkbox shows 'None' CLE entry", async () => {
    await userEvent.click(noCleCheckbox);

    expect(mockTokenfield.emptyItems).toHaveBeenCalled();
    expect(tokenFieldInput).toHaveStyle("display: none");
    expect(tokenFieldSetList).toContainHTML(
      `<li class="tokenfield-set-item tau-none-item"><span class="item-label">None</span><a class="item-remove" tabindex="-1">×</a></li>`
    );
  });

  test("Unchecking no cle checkbox removes 'None' CLE entry", async () => {
    await userEvent.click(noCleCheckbox);
    await userEvent.click(noCleCheckbox);
    expect(tokenFieldInput).not.toHaveStyle("display: none");
    expect(tokenFieldSetList).toBeEmptyDOMElement();
  });

  test("Click 'None' CLE entry removes 'None' CLE entry", async () => {
    await userEvent.click(noCleCheckbox);
    const noneEntry = document.querySelector(".item-remove");
    await userEvent.click(noneEntry);
    expect(tokenFieldInput).not.toHaveStyle("display: none");
    expect(tokenFieldSetList).toBeEmptyDOMElement();
  });

  test("Calling reset removes 'None' CLE entry", async () => {
    await userEvent.click(noCleCheckbox);
    component.reset();
    expect(tokenFieldInput).not.toHaveStyle("display: none");
    expect(tokenFieldSetList).toBeEmptyDOMElement();
  });
});
