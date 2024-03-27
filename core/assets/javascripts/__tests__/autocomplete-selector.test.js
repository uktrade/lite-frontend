import "@testing-library/jest-dom";
import { waitFor } from "@testing-library/dom";
import AutoCompleteSelector from "../autocomplete-selector";

const createElements = () => {
  document.body.innerHTML = `
    <div id="container" name="test">
      <select id="country-autocomplete">
        <option value=""></option>
        <option value="1">One</option>
        <option value="2">Two</option>
        <option value="3">Three</option>
      </select>
    </div>
  `;

  return document.querySelector("#country-autocomplete");
};

describe("AutoCompleteSelector", () => {
  test("Calling accessible autocomplete", async () => {
    const $el = createElements();
    new AutoCompleteSelector($el).init();
    await waitFor(() => {
      const $wrapper = document.querySelector(".lite-autocomplete__wrapper");

      expect($wrapper).not.toBe(null);
      expect($el).not.toBeVisible();
    });
  });

  test("Calling accessible example values", async () => {
    const $el = createElements();
    new AutoCompleteSelector($el).init();

    await waitFor(() => {
      document.querySelector(".lite-autocomplete__wrapper input").value = "e";
      let suggestions = document.querySelectorAll(
        ".lite-autocomplete__wrapper li"
      );
      expect(suggestions[0].textContent).toBe("One");
      expect(suggestions[1].textContent).toBe("Three");
    });
  });
});
