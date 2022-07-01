import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import SelectProducts from "../select-products";

let checkboxes, spy;

const createElements = () => {
  document.body.innerHTML = `
    <div>
      <input type="checkbox" name="checkbox-1" value="checkbox-1" data-script-id="product-1" />
      <script id="product-1-name">"Product A"</script>
      <script id="product-1-control-list-entries">[{"rating": "R1"}, {"rating": "R1a"}]</script>
      <input type="checkbox" name="checkbox-2" value="checkbox-2" data-script-id="product-2" />
      <script id="product-2-name">"Product B"</script>
      <script id="product-2-control-list-entries">[{"rating": "R2"}, {"rating": "R2a"}]</script>
      <input type="checkbox" name="checkbox-3" value="checkbox-3" data-script-id="product-3" />
      <script id="product-3-name">"Product C"</script>
      <script id="product-3-control-list-entries">[{"rating": "R3"}, {"rating": "R3a"}]</script>
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
