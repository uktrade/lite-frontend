import { progressivelyEnhanceMultipleSelectFieldStartsWith } from "../multi-select";
// make a document with a basic dropdown to instantiate and filter with tokenfield

const createElements = () => {
  document.body.innerHTML = `
    <select
    id="select"
    >
        <option value="12345">
            damien
        </option>
        <option value="1234">
            Daniel
        </option>
        <option value="123">
            adam
        </option>
        <option value="678">
            Mathew (DDAT)
        </option>
    </select>
    `;

  const element = document.querySelector("#select");
  return element;
};

describe("Test progressivelyEnhanceMultipleSelectFieldStartsWith input", () => {
  beforeEach(() => {
    const element = createElements();
    const tokenField = progressivelyEnhanceMultipleSelectFieldStartsWith(
      element,
      (option) => {
        return { id: option.value, name: option.label, classes: [] };
      }
    );
  });

  test("_filterData a", () => {
    const expected = ["adam", "damien", "Daniel", "Mathew (DDAT)"];
    document.querySelector(".tokenfield-input").value = "a";
    document.querySelector(".tokenfield-input").click();
    const results = Array.from(
      document.querySelectorAll(".tokenfield-suggest-item")
    ).map((item) => item.innerHTML);
    expect(results).toStrictEqual(expected);
  });

  test("input: da", () => {
    const expected = ["damien", "Daniel", "adam", "Mathew (DDAT)"];
    document.querySelector(".tokenfield-input").value = "da";
    document.querySelector(".tokenfield-input").click();
    const results = Array.from(
      document.querySelectorAll(".tokenfield-suggest-item")
    ).map((item) => item.innerHTML);
    expect(results).toStrictEqual(expected);
  });

  test("input: am", () => {
    const expected = ["adam", "damien"];
    document.querySelector(".tokenfield-input").value = "am";
    document.querySelector(".tokenfield-input").click();
    const results = Array.from(
      document.querySelectorAll(".tokenfield-suggest-item")
    ).map((item) => item.innerHTML);
    expect(results).toStrictEqual(expected);
  });

  test("input: ddat", () => {
    const expected = ["Mathew (DDAT)"];
    document.querySelector(".tokenfield-input").value = "ddat";
    document.querySelector(".tokenfield-input").click();
    var results = Array.from(
      document.querySelectorAll(".tokenfield-suggest-item")
    ).map((item) => item.innerHTML);
    expect(results).toStrictEqual(expected);

    document.querySelector(".tokenfield-input").value = "DDAT";
    document.querySelector(".tokenfield-input").click();
    var results = Array.from(
      document.querySelectorAll(".tokenfield-suggest-item")
    ).map((item) => item.innerHTML);
    expect(results).toStrictEqual(expected);
  });
});
