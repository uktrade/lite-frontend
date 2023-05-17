import { getByText } from "@testing-library/dom";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import { Customiser } from "../customiser";

const createElement = () => {
  document.body.innerHTML = `
    <div class="customiser" data-customiser-spec='{"options_label": "Customise list", "identifier": "list-view", "toggleable_elements": [{"key": "thrace", "label": "Thrace"}, {"key": "tigh", "label": "Tighs", "default_visible": true}, {"key": "adama", "label": "Adamas", "default_visible": true}]}'>

      <div class="customiser__header">
      </div>

      <ol>
        <li id="bill" data-customiser-key="adama">Bill</li>
        <li id="lee" data-customiser-key="adama">Lee</li>
        <li id="joseph" data-customiser-key="adama">Joseph</li>
        <li id="saul" data-customiser-key="tigh">Saul</li>
        <li id="ellen" data-customiser-key="tigh">Ellen</li>
        <li id="kara" data-customiser-key="thrace">Kara</li>
      </ol>
    </div>
  `;
  return document.querySelector("div");
};

const createComponent = (numItems, visibleElems) => {
  let div = createElement();
  new Customiser(div).init();
  return div;
};

describe("Customiser", () => {
  test("Customiser options are displayed correctly", () => {
    window.localStorage.clear();
    const div = createComponent();
    const optionsDiv = div.querySelector("div.customiser__header");

    const adamasOption = getByText(optionsDiv, "Adamas").parentElement;
    const adamasCheckbox = adamasOption.querySelector("input");
    expect(adamasCheckbox).toHaveAttribute("checked");

    const tighsOption = getByText(optionsDiv, "Tighs").parentElement;
    const tighsCheckbox = tighsOption.querySelector("input");
    expect(tighsCheckbox).toHaveAttribute("checked");

    const thraceOption = getByText(optionsDiv, "Thrace").parentElement;
    const thraceCheckbox = thraceOption.querySelector("input");
    expect(thraceCheckbox).not.toHaveAttribute("checked");
  });

  test("Default elements are visible before any interaction", () => {
    window.localStorage.clear();
    const div = createComponent();
    const ol = div.querySelector("ol");

    const visibleElementIds = ["bill", "lee", "joseph", "saul", "ellen"];
    visibleElementIds.forEach((id) => {
      const elem = ol.querySelector("#" + id);
      expect(elem).not.toHaveClass("customiser__toggleable--hidden");
    });

    const hiddenElementIds = ["kara"];
    hiddenElementIds.forEach((id) => {
      const elem = ol.querySelector("#" + id);
      expect(elem).toHaveClass("customiser__toggleable--hidden");
    });
  });

  test("Ticking/unticking options shows/hides elements properly", async () => {
    window.localStorage.clear();
    const div = createComponent();
    const optionsDiv = div.querySelector("div.customiser__header");
    const ol = div.querySelector("ol");

    const adamasOption = getByText(optionsDiv, "Adamas").parentElement;
    const adamasCheckbox = adamasOption.querySelector("input");
    expect(adamasCheckbox).toHaveAttribute("checked");

    const adamaElementIds = ["bill", "lee", "joseph"];
    // Check the elements are visible to start with
    adamaElementIds.forEach((id) => {
      const elem = ol.querySelector("#" + id);
      expect(elem).not.toHaveClass("customiser__toggleable--hidden");
    });
    // Click the option
    await userEvent.click(adamasCheckbox);
    // Check the elements are now not visible
    adamaElementIds.forEach((id) => {
      const elem = ol.querySelector("#" + id);
      expect(elem).toHaveClass("customiser__toggleable--hidden");
    });

    const thraceOption = getByText(optionsDiv, "Thrace").parentElement;
    const thraceCheckbox = thraceOption.querySelector("input");
    expect(thraceCheckbox).not.toHaveAttribute("checked");
    const thraceElementIds = ["kara"];
    // Check the elements are not visible to start with
    thraceElementIds.forEach((id) => {
      const elem = ol.querySelector("#" + id);
      expect(elem).toHaveClass("customiser__toggleable--hidden");
    });
    // Click the option
    await userEvent.click(thraceCheckbox);
    // Check the elements are now visible
    thraceElementIds.forEach((id) => {
      const elem = ol.querySelector("#" + id);
      expect(elem).not.toHaveClass("customiser__toggleable--hidden");
    });
  });

  test("Choices are persisted between page loads", async () => {
    window.localStorage.clear();
    let div = createComponent();
    let optionsDiv = div.querySelector("div.customiser__header");
    let ol = div.querySelector("ol");

    let thraceOption = getByText(optionsDiv, "Thrace").parentElement;
    let thraceCheckbox = thraceOption.querySelector("input");
    expect(thraceCheckbox).not.toHaveAttribute("checked");
    const thraceElementIds = ["kara"];
    // Check the elements are not visible to start with
    thraceElementIds.forEach((id) => {
      const elem = ol.querySelector("#" + id);
      expect(elem).toHaveClass("customiser__toggleable--hidden");
    });
    // Click the option
    await userEvent.click(thraceCheckbox);
    // Check the elements are now visible
    thraceElementIds.forEach((id) => {
      const elem = ol.querySelector("#" + id);
      expect(elem).not.toHaveClass("customiser__toggleable--hidden");
    });

    // recreate the element
    div = createComponent();
    // expect the choice to have been persisted
    optionsDiv = div.querySelector("div.customiser__header");
    ol = div.querySelector("ol");

    thraceOption = getByText(optionsDiv, "Thrace").parentElement;
    thraceCheckbox = thraceOption.querySelector("input");
    expect(thraceCheckbox).toHaveAttribute("checked");

    // expect the elements to be visible
    thraceElementIds.forEach((id) => {
      const elem = ol.querySelector("#" + id);
      expect(elem).not.toHaveClass("customiser__toggleable--hidden");
    });
  });
});
