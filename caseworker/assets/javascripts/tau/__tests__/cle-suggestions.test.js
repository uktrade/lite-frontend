import { getAllByText, getByText } from "@testing-library/dom";
import userEvent from "@testing-library/user-event";
import "@testing-library/jest-dom";

import CLESuggestions from "../cle-suggestions";

let buttonContainer, component, callbackSpy;

const createElements = () => {
  document.body.innerHTML = `
    <div id="button-container"></div>
  `;

  return document.querySelector("#button-container");
};

const createComponent = () => {
  callbackSpy = jest.fn();
  buttonContainer = createElements();
  component = new CLESuggestions(buttonContainer, callbackSpy);
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

  test("Set multiple products", () => {
    component.setProducts([
      {
        controlListEntries: [
          { id: "1", rating: "R1" },
          { id: "2", rating: "R1a" },
        ],
      },
      {
        controlListEntries: [
          { id: "3", rating: "R2" },
          { id: "4", rating: "R2a" },
        ],
      },
      {
        controlListEntries: [
          { id: "5", rating: "R3" },
          { id: "6", rating: "R3a" },
        ],
      },
    ]);
    expect(buttonContainer).toContainHTML(
      `<button class="lite-button--link">Select exporter suggestion R1, R1a</button>`
    );
    expect(buttonContainer).toContainHTML(
      `<button class="lite-button--link">Select exporter suggestion R2, R2a</button>`
    );
    expect(buttonContainer).toContainHTML(
      `<button class="lite-button--link">Select exporter suggestion R3, R3a</button>`
    );
  });

  test("Duplicates removed", () => {
    component.setProducts([
      {
        controlListEntries: [{ id: "1", rating: "R3" }],
      },
      {
        controlListEntries: [{ id: "1", rating: "R3" }],
      },
      {
        controlListEntries: [
          { id: "2", rating: "R1" },
          { id: "3", rating: "R1a" },
        ],
      },
      {
        controlListEntries: [
          { id: "2", rating: "R1" },
          { id: "3", rating: "R1a" },
        ],
      },
      {
        // This isn't really a duplicate even though the previous entries are in other CLEs as we use the whole group to
        // test for duplication
        controlListEntries: [
          { id: "1", rating: "R3" },
          { id: "3", rating: "R1a" },
        ],
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
        controlListEntries: [
          { id: "1", rating: "R1" },
          { id: "2", rating: "R1a" },
        ],
      },
      {
        controlListEntries: [
          { id: "2", rating: "R1a" },
          { id: "1", rating: "R1" },
        ],
      },
    ]);
    expect(
      getAllByText(buttonContainer, "Select exporter suggestion R1, R1a").length
    ).toEqual(1);
  });

  test("Callback called on button click", async () => {
    component.setProducts([
      {
        controlListEntries: [
          { id: "1", rating: "R1" },
          { id: "2", rating: "R1a" },
        ],
      },
      {
        controlListEntries: [
          { id: "3", rating: "R2" },
          { id: "4", rating: "R2a" },
        ],
      },
      {
        controlListEntries: [
          { id: "5", rating: "R3" },
          { id: "6", rating: "R3a" },
        ],
      },
    ]);
    await userEvent.click(
      getByText(buttonContainer, "Select exporter suggestion R1, R1a")
    );
    expect(callbackSpy).toHaveBeenCalledWith([
      { id: "1", rating: "R1" },
      { id: "2", rating: "R1a" },
    ]);
    await userEvent.click(
      getByText(buttonContainer, "Select exporter suggestion R2, R2a")
    );
    expect(callbackSpy).toHaveBeenCalledWith([
      { id: "3", rating: "R2" },
      { id: "4", rating: "R2a" },
    ]);
    await userEvent.click(
      getByText(buttonContainer, "Select exporter suggestion R3, R3a")
    );
    expect(callbackSpy).toHaveBeenCalledWith([
      { id: "5", rating: "R3" },
      { id: "6", rating: "R3a" },
    ]);
  });
});
