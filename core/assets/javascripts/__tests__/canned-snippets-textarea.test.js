import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import CannedSnippetsTextArea from "../canned-snippets-textarea";

const createComponent = ($div) => {
  return new CannedSnippetsTextArea($div);
};

describe("Canned snippets textarea", () => {
  test("Clicking snippet appends text", async () => {
    document.body.innerHTML = `
    <div data-module="canned-snippets-textarea">
      <textarea name="text">Some starting text</textarea>
      <p>
        Snippet 1
        <a data-snippet-key="snippet_1">Add</a>
      </p>
      <p>
        Snippet 2
        <a data-snippet-key="snippet_2">Add</a>
      </p>
      <script type="application/json">{"snippet_1": "snippet 1 text", "snippet_2": "snippet 2 text"}</script>
    </div>
    `;

    const $textarea = document.querySelector("textarea");
    const $div = document.querySelector("div");
    const component = createComponent($div);

    component.init();
    const addSnippet1 = document.querySelector("a[data-snippet-key=snippet_1]");
    const addSnippet2 = document.querySelector("a[data-snippet-key=snippet_2]");
    await userEvent.click(addSnippet1);
    expect($textarea.value).toBe(
      `snippet 1 text

--------
Some starting text`,
    );
    await userEvent.click(addSnippet2);
    expect($textarea.value).toBe(
      `snippet 2 text

--------
snippet 1 text

--------
Some starting text`,
    );
  });
});
