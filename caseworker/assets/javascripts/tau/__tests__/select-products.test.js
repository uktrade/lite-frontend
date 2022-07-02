import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import SelectProducts from "../select-products";

let checkboxes, spy;

const products = [
  {
    id: "checkbox-1",
    name: "Product A",
    control_list_entries: [{ rating: "R1" }, { rating: "R1a" }],
  },
  {
    id: "checkbox-2",
    name: "Product B",
    control_list_entries: [{ rating: "R2" }, { rating: "R2a" }],
  },
  {
    id: "checkbox-3",
    name: "Product C",
    control_list_entries: [{ rating: "R3" }, { rating: "R3a" }],
  },
];

const createElements = () => {
  document.body.innerHTML = `
    <div>
      <input type="checkbox" name="checkbox-1" value="checkbox-1" />
      <input type="checkbox" name="checkbox-2" value="checkbox-2" />
      <input type="checkbox" name="checkbox-3" value="checkbox-3" />
    </div>
  `;

  return document.querySelectorAll("[type=checkbox]");
};

const createComponent = () => {
  checkboxes = createElements();
  spy = jest.fn();
  const selectProducts = new SelectProducts(
    checkboxes,
    products,
    (selectedProducts) => spy(selectedProducts)
  );
  selectProducts.init();
  return selectProducts;
};

test("Products set on init", async () => {
  const checkboxes = createElements();
  for (const checkbox of checkboxes) {
    await userEvent.click(checkbox);
  }
  const spy = jest.fn();
  new SelectProducts(checkboxes, products, (selectedProducts) =>
    spy(selectedProducts)
  ).init();
  expect(spy).toBeCalledWith([
    {
      name: "Product A",
      controlListEntries: [{ rating: "R1" }, { rating: "R1a" }],
    },
    {
      name: "Product B",
      controlListEntries: [{ rating: "R2" }, { rating: "R2a" }],
    },
    {
      name: "Product C",
      controlListEntries: [{ rating: "R3" }, { rating: "R3a" }],
    },
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
    expect(spy).toBeCalledWith([
      {
        name: "Product A",
        controlListEntries: [{ rating: "R1" }, { rating: "R1a" }],
      },
    ]);

    await userEvent.click(checkboxes[1]);
    expect(spy).toBeCalledWith([
      {
        name: "Product A",
        controlListEntries: [{ rating: "R1" }, { rating: "R1a" }],
      },
      {
        name: "Product B",
        controlListEntries: [{ rating: "R2" }, { rating: "R2a" }],
      },
    ]);

    await userEvent.click(checkboxes[2]);
    expect(spy).toBeCalledWith([
      {
        name: "Product A",
        controlListEntries: [{ rating: "R1" }, { rating: "R1a" }],
      },
      {
        name: "Product B",
        controlListEntries: [{ rating: "R2" }, { rating: "R2a" }],
      },
      {
        name: "Product C",
        controlListEntries: [{ rating: "R3" }, { rating: "R3a" }],
      },
    ]);

    await userEvent.click(checkboxes[0]);
    expect(spy).toBeCalledWith([
      {
        name: "Product B",
        controlListEntries: [{ rating: "R2" }, { rating: "R2a" }],
      },
      {
        name: "Product C",
        controlListEntries: [{ rating: "R3" }, { rating: "R3a" }],
      },
    ]);

    await userEvent.click(checkboxes[1]);
    expect(spy).toBeCalledWith([
      {
        name: "Product C",
        controlListEntries: [{ rating: "R3" }, { rating: "R3a" }],
      },
    ]);

    await userEvent.click(checkboxes[2]);
    expect(spy).toBeCalledWith([]);
  });
});
