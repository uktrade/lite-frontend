import { getByText } from "@testing-library/dom";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import { ListExpander } from "../list-expander";

const createElement = (numItems, visibleElems) => {
  let allItems = ``;
  for (let i = 1; i <= numItems; i++) {
    allItems +=
      `
      <li class="expander__expand-list__item">` +
      "Item " +
      i +
      `
      </li>
    `;
  }

  document.body.innerHTML =
    `
    <div class="expander" data-expander-visible-elems="` +
    visibleElems +
    `">

      <ul class="expander__expand-list">` +
    allItems +
    `
      </ul>
    </div>
  `;
  return document.querySelector("div");
};

const createComponent = (numItems, visibleElems) => {
  let div = createElement(numItems, visibleElems);
  new ListExpander(div).init();
  return div;
};

describe("List expander", () => {
  test("Elements below the line are not visible", () => {
    const div = createComponent(2, 1);

    const item1 = getByText(div, "Item 1");
    expect(item1).not.toHaveClass("expander__expand-list__item__hidden");
    expect(item1).not.toHaveAttribute("aria-hidden");

    const item2 = getByText(div, "Item 2");
    expect(item2).toHaveClass("expander__expand-list__item__hidden");
    expect(item2).toHaveAttribute("aria-hidden", "false");
    expect(item1).not.toHaveAttribute("aria-hidden");

    const expandButton = div.querySelector("button");
    expect(expandButton).toBeInTheDocument();
  });

  test("Expander with no hidden elements has no visible expand button", () => {
    const div = createComponent(2, 2);

    const item1 = getByText(div, "Item 1");
    expect(item1).not.toHaveClass("expander__expand-list__item__hidden");

    const item2 = getByText(div, "Item 2");
    expect(item2).not.toHaveClass("expander__expand-list__item__hidden");

    const expandButton = div.querySelector("button");
    expect(expandButton).not.toBeInTheDocument();
  });

  test("Expander with hidden elements has correct button text", () => {
    const div = createComponent(2, 1);

    const expandButton = div.querySelector("button");
    expect(expandButton).toBeInTheDocument();
    expect(expandButton).toHaveTextContent("1 of 2");
  });

  test("Expander with hidden elements shows elements on click of button", async () => {
    const div = createComponent(2, 1);

    const item1 = getByText(div, "Item 1");
    expect(item1).not.toHaveClass("expander__expand-list__item__hidden");

    const item2 = getByText(div, "Item 2");
    expect(item2).toHaveClass("expander__expand-list__item__hidden");

    const expandButton = div.querySelector("button");
    expect(expandButton).toBeInTheDocument();
    await userEvent.click(expandButton);

    expect(item1).not.toHaveClass("expander__expand-list__item__hidden");
    expect(item2).not.toHaveClass("expander__expand-list__item__hidden");
    expect(expandButton).not.toBeInTheDocument();
  });
});
