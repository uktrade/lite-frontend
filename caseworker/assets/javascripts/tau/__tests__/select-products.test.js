import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import SelectProducts from "../select-products";

let checkboxes, spy;

const createElements = () => {
  document.body.innerHTML = `
    <div>
      <input type="checkbox" name="checkbox-1" value="checkbox-1" data-product-name="Product A" />
      <input type="checkbox" name="checkbox-2" value="checkbox-2" data-product-name="Product B" />
      <input type="checkbox" name="checkbox-3" value="checkbox-3" data-product-name="Product C" />
    </div>
  `;

  return document.querySelectorAll("[type=checkbox]");
};

const createComponent = () => {
  checkboxes = createElements();
  spy = jest.fn();
  return new SelectProducts(checkboxes, (selectedProducts) =>
    spy(selectedProducts)
  ).init();
};

test("Products set on init", async () => {
  const checkboxes = createElements();
  for (const checkbox of checkboxes) {
    await userEvent.click(checkbox);
  }
  const spy = jest.fn();
  new SelectProducts(checkboxes, (selectedProducts) =>
    spy(selectedProducts)
  ).init();
  expect(spy).toBeCalledWith([
    { name: "Product A" },
    { name: "Product B" },
    { name: "Product C" },
  ]);
});

describe("Select products", () => {
  beforeEach(() => {
    createComponent();
  });

  afterEach(() => {
    spy.mockReset();
  });

  test("Clicking checkboxes", async () => {
    await userEvent.click(checkboxes[0]);
    expect(spy).toBeCalledWith([{ name: "Product A" }]);

    await userEvent.click(checkboxes[1]);
    expect(spy).toBeCalledWith([{ name: "Product A" }, { name: "Product B" }]);

    await userEvent.click(checkboxes[2]);
    expect(spy).toBeCalledWith([
      { name: "Product A" },
      { name: "Product B" },
      { name: "Product C" },
    ]);

    await userEvent.click(checkboxes[0]);
    expect(spy).toBeCalledWith([{ name: "Product B" }, { name: "Product C" }]);

    await userEvent.click(checkboxes[1]);
    expect(spy).toBeCalledWith([{ name: "Product C" }]);

    await userEvent.click(checkboxes[2]);
    expect(spy).toBeCalledWith([]);
  });
});
