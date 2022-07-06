import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import ExpandAll from "../expand-all";

let expandAllButton, details;

const createElements = () => {
  document.body.innerHTML = `
    <div>
      <button id="expand-all-button">Show all</button>
      <div id="details">
        <details>
          <summary>Summary 1</summary>
          Details 1
        </details>
        <details>
          <summary>Summary 2</summary>
          Details 2
        </details>
        <details>
          <summary>Summary 3</summary>
          Details 3
        </details>
      </div>
    </div>
  `;

  const _expandAllButton = document.querySelector("#expand-all-button");
  const _details = document.querySelectorAll("#details details");

  return [_expandAllButton, _details];
};

const createComponent = () => {
  [expandAllButton, details] = createElements();
  return new ExpandAll(expandAllButton, details).init();
};

test("Details set before init sets button text", () => {
  [expandAllButton, details] = createElements();
  for (const detail of details) {
    detail.open = true;
  }
  new ExpandAll(expandAllButton, details).init();
  expect(expandAllButton).toHaveTextContent("Hide all");
});

describe("Expand all", () => {
  beforeEach(() => {
    createComponent();
  });

  test("Clicking expand all", async () => {
    await userEvent.click(expandAllButton);
    expect(expandAllButton).toHaveTextContent("Hide all");
    for (const detail of details) {
      expect(detail).toHaveAttribute("open");
    }
  });

  test("Clicking expand all and then hide all", async () => {
    await userEvent.click(expandAllButton);
    expect(expandAllButton).toHaveTextContent("Hide all");
    for (const detail of details) {
      expect(detail).toHaveAttribute("open");
    }

    await userEvent.click(expandAllButton);
    expect(expandAllButton).toHaveTextContent("Show all");
    for (const detail of details) {
      expect(detail).not.toHaveAttribute("open");
    }
  });

  test("Opening all sets button", async () => {
    for (const detail of details) {
      const summary = detail.querySelector("summary");
      await userEvent.click(summary);
    }
    expect(expandAllButton).toHaveTextContent("Hide all");
  });

  test("Opening all then hiding one sets button", async () => {
    for (const detail of details) {
      const summary = detail.querySelector("summary");
      await userEvent.click(summary);
    }
    const summary = details[0].querySelector("summary");
    await userEvent.click(summary);
    expect(expandAllButton).toHaveTextContent("Show all");
  });

  test("Toggle events called when opening and closing all", async () => {
    for (const detail of details) {
      const toggleSpy = jest.fn();
      detail.addEventListener("toggle", () => toggleSpy());
      const summary = detail.querySelector("summary");
      await userEvent.click(summary);
      expect(toggleSpy).toHaveBeenCalled();
    }
  });
});
