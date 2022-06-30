import "@testing-library/jest-dom";

import Headline from "../headline";

let headline, component;

const createElements = () => {
  document.body.innerHTML = `
    <div id="headline"></div>
  `;

  headline = document.querySelector("#headline");

  return headline;
};

const createComponent = () => {
  headline = createElements();
  component = new Headline(headline);
  return component;
};

describe("Headline", () => {
  beforeEach(() => {
    createComponent();
  });

  test("Default", () => {
    expect(headline).toHaveTextContent("");
  });

  test("Set no products", () => {
    component.setProducts([]);
    expect(headline).toHaveTextContent("Assessing 0 products");
  });

  test("Set single product", () => {
    component.setProducts([{ name: "Product A" }]);
    expect(headline).toHaveTextContent("Assessing Product A");
  });

  test("Set multiple products", () => {
    component.setProducts([{ name: "Product A" }, { name: "Product B" }]);
    expect(headline).toHaveTextContent("Assessing 2 products");

    component.setProducts([
      { name: "Product A" },
      { name: "Product B" },
      { name: "Product C" },
    ]);
    expect(headline).toHaveTextContent("Assessing 3 products");
  });
});
