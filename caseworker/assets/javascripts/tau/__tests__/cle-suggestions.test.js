import { getAllByText, getByText } from "@testing-library/dom";
import userEvent from "@testing-library/user-event";
import "@testing-library/jest-dom";

import CLESuggestions from "../cle-suggestions";

let buttonContainer, component;

const createElements = () => {
  document.body.innerHTML = `
    <div id="button-container"></div>
  `;

  return document.querySelector("#button-container");
};

const createComponent = () => {
  buttonContainer = createElements();
  component = new CLESuggestions(buttonContainer);
  return component;
};

describe("CLE suggestions", () => {
  beforeEach(() => {
    createComponent();
  });

  test("Default", () => {
    expect(buttonContainer).toBeEmptyDOMElement();
  });

  test("Set no products", () => {
    component.setProducts([]);
    expect(buttonContainer).toBeEmptyDOMElement();
  });

  test("Set product with no exporter CLE entry", () => {
    component.setProducts([
      {
        controlListEntries: {
          exporter: [],
        },
      },
    ]);
    expect(buttonContainer).toBeEmptyDOMElement();
  });

  test("Set multiple exporter CLE products", () => {
    component.setProducts([
      {
        controlListEntries: {
          exporter: ["R1", "R1a"],
        },
      },
      {
        controlListEntries: {
          exporter: ["R2", "R2a"],
        },
      },
      {
        controlListEntries: {
          exporter: ["R3", "R3a"],
        },
      },
    ]);
    expect(buttonContainer).toContainHTML(
      `<button class="lite-button--link" type="button">Select exporter suggestion R1, R1a</button>`
    );
    expect(buttonContainer).toContainHTML(
      `<button class="lite-button--link" type="button">Select exporter suggestion R2, R2a</button>`
    );
    expect(buttonContainer).toContainHTML(
      `<button class="lite-button--link" type="button">Select exporter suggestion R3, R3a</button>`
    );
  });

  test("Duplicates removed", () => {
    component.setProducts([
      {
        controlListEntries: {
          exporter: ["R3"],
        },
      },
      {
        controlListEntries: {
          exporter: ["R3"],
        },
      },
      {
        controlListEntries: {
          exporter: ["R1", "R1a"],
        },
      },
      {
        controlListEntries: {
          exporter: ["R1", "R1a"],
        },
      },
      {
        // This isn't really a duplicate even though the previous entries are in other CLEs as we use the whole group to
        // test for duplication
        controlListEntries: {
          exporter: ["R3", "R1a"],
        },
      },
    ]);
    expect(
      getAllByText(buttonContainer, "Select exporter suggestion R3").length
    ).toEqual(1);
    expect(
      getAllByText(buttonContainer, "Select exporter suggestion R1, R1a").length
    ).toEqual(1);
    expect(
      getAllByText(buttonContainer, "Select exporter suggestion R3, R1a").length
    ).toEqual(1);
  });

  test("Reordered ratings considered duplicate", () => {
    component.setProducts([
      {
        controlListEntries: {
          exporter: ["R1", "R1a"],
        },
      },
      {
        controlListEntries: {
          exporter: ["R1a", "R1"],
        },
      },
    ]);
    expect(
      getAllByText(buttonContainer, "Select exporter suggestion R1, R1a").length
    ).toEqual(1);
  });

  test("Callback called on button click", async () => {
    const callbackSpy = jest.fn();
    component.on("change", (suggestion) => callbackSpy(suggestion));
    component.setProducts([
      {
        controlListEntries: {
          exporter: ["R1", "R1a"],
        },
      },
      {
        controlListEntries: {
          exporter: ["R2", "R2a"],
        },
      },
      {
        controlListEntries: {
          exporter: ["R3", "R3a"],
        },
      },
    ]);
    await userEvent.click(
      getByText(buttonContainer, "Select exporter suggestion R1, R1a")
    );
    expect(callbackSpy).toHaveBeenCalledWith(["R1", "R1a"]);
    await userEvent.click(
      getByText(buttonContainer, "Select exporter suggestion R2, R2a")
    );
    expect(callbackSpy).toHaveBeenCalledWith(["R2", "R2a"]);
    await userEvent.click(
      getByText(buttonContainer, "Select exporter suggestion R3, R3a")
    );
    expect(callbackSpy).toHaveBeenCalledWith(["R3", "R3a"]);
  });

  test("Setting product with blank precedents CLE entries", () => {
    component.setProducts([
      {
        controlListEntries: {
          precedents: [[]],
        },
      },
    ]);
    expect(buttonContainer).toBeEmptyDOMElement();
  });

  test("Setting product with precedents CLE entries", () => {
    component.setProducts([
      {
        controlListEntries: {
          precedents: [["R1", "R1a"]],
        },
      },
      {
        controlListEntries: {
          precedents: [
            ["R2", "R2a"],
            ["R3", "R3a"],
          ],
        },
      },
    ]);
    expect(buttonContainer).toContainHTML(
      `<button class="lite-button--link" type="button">Copy previous assessment R1, R1a</button>`
    );
    expect(buttonContainer).toContainHTML(
      `<button class="lite-button--link" type="button">Copy previous assessment R2, R2a</button>`
    );
    expect(buttonContainer).toContainHTML(
      `<button class="lite-button--link" type="button">Copy previous assessment R3, R3a</button>`
    );
  });

  test("Setting product with mixed CLE entries", () => {
    component.setProducts([
      {
        controlListEntries: {
          exporter: ["R1", "R1a"],
        },
      },
      {
        controlListEntries: {
          precedents: [
            ["R2", "R2a"],
            ["R3", "R3a"],
          ],
        },
      },
    ]);
    expect(buttonContainer).toContainHTML(
      `<button class="lite-button--link" type="button">Select exporter suggestion R1, R1a</button>`
    );
    expect(buttonContainer).toContainHTML(
      `<button class="lite-button--link" type="button">Copy previous assessment R2, R2a</button>`
    );
    expect(buttonContainer).toContainHTML(
      `<button class="lite-button--link" type="button">Copy previous assessment R3, R3a</button>`
    );
  });

  test("Setting product with mixed duplicated CLE entries", () => {
    component.setProducts([
      {
        controlListEntries: {
          exporter: ["R1", "R1a"],
        },
      },
      {
        controlListEntries: {
          precedents: [["R1", "R1a"]],
        },
      },
    ]);
    expect(buttonContainer).toContainHTML(
      `<button class="lite-button--link" type="button">Select exporter suggestion R1, R1a</button>`
    );
    expect(buttonContainer).toContainHTML(
      `<button class="lite-button--link" type="button">Copy previous assessment R1, R1a</button>`
    );
  });
});
