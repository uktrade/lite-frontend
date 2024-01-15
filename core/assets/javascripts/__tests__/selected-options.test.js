import "@testing-library/jest-dom";
import { getAllByText } from "@testing-library/dom";

import userEvent from "@testing-library/user-event";
import SelectedOptions from "../selected-options";

const createElements = () => {
  document.body.innerHTML = `
    <div>
      <div id="container"></div>
      <select id="multi-select" multiple>
        <option value="1">One</option>
        <option value="2">Two</option>
        <option value="3">Three</option>
      </select>
    </div>
  `;

  return [
    document.querySelector("#container"),
    document.querySelector("#multi-select"),
  ];
};

describe("Selected options", () => {
  let user;
  beforeEach(() => {
    user = userEvent.setup();
  });

  test("Renders list on init", () => {
    const [$container, $multiSelect] = createElements();

    const selectedOptions = new SelectedOptions(
      $container,
      $multiSelect,
      "objects"
    );

    expect($container).toBeEmptyDOMElement();
    selectedOptions.init();

    const $wrapper = $container.querySelector("div");
    expect($container).toContainElement($wrapper);
    expect($wrapper.ariaLive).toEqual("polite");
    expect($wrapper).toHaveClass("selected-options");
    expect($wrapper).toHaveClass("selected-options--empty");

    const $p = $wrapper.querySelector("p");
    expect($p).toHaveTextContent("Selected objects");
    expect($p).toHaveClass("govuk-visually-hidden");

    const $ul = $wrapper.querySelector("ul");
    expect($ul).toBeEmptyDOMElement();
    expect($ul).toHaveClass("selected-options__options");
  });

  test("Renders list with selected items on init", () => {
    const [$container, $multiSelect] = createElements();

    const selectedOptions = new SelectedOptions($container, $multiSelect);

    $multiSelect.options[0].selected = true;
    $multiSelect.options[2].selected = true;

    expect($container).toBeEmptyDOMElement();

    selectedOptions.init();
    const $wrapper = $container.querySelector("div");
    expect($wrapper).not.toHaveClass("selected-options--empty");
    const $ul = $container.querySelector("ul");
    expect($container).toContainElement($ul);
    expect($ul).not.toBeEmptyDOMElement();

    const $lis = $ul.querySelectorAll("li");
    expect($lis).toHaveLength(2);
    expect($lis[0]).toHaveTextContent("One");
    expect($lis[1]).toHaveTextContent("Three");
    for (const $li of $lis) {
      expect($li).toHaveClass("selected-options__option");
    }
  });

  test("Changing select options updates", async () => {
    const [$container, $multiSelect] = createElements();

    const selectedOptions = new SelectedOptions($container, $multiSelect);
    selectedOptions.init();
    const $wrapper = $container.querySelector("div");

    await user.selectOptions($multiSelect, ["1"]);
    let $ul = $container.querySelector("ul");
    let $lis = $ul.querySelectorAll("li");
    expect($lis).toHaveLength(1);
    expect($lis[0]).toHaveTextContent("One");
    expect($wrapper).not.toHaveClass("selected-options--empty");

    await user.selectOptions($multiSelect, ["3"]);
    $ul = $container.querySelector("ul");
    $lis = $ul.querySelectorAll("li");
    expect($lis).toHaveLength(2);
    expect($lis[0]).toHaveTextContent("One");
    expect($lis[1]).toHaveTextContent("Three");
    expect($wrapper).not.toHaveClass("selected-options--empty");

    await user.deselectOptions($multiSelect, ["1", "3"]);
    $ul = $container.querySelector("ul");
    $lis = $ul.querySelectorAll("li");
    expect($lis).toHaveLength(0);
    expect($wrapper).toHaveClass("selected-options--empty");
  });

  test("Removing options updates", async () => {
    const [$container, $multiSelect] = createElements();

    const selectedOptions = new SelectedOptions($container, $multiSelect);

    const onChangeSpy = jest.fn();
    $multiSelect.addEventListener("change", () => onChangeSpy());

    $multiSelect.options[0].selected = true;
    $multiSelect.options[2].selected = true;

    selectedOptions.init();

    let $ul = $container.querySelector("ul");
    let $lis = $ul.querySelectorAll("li");
    expect($lis).toHaveLength(2);

    const $removeButtons = getAllByText($ul, "Remove");
    for (const $removeButton of $removeButtons) {
      expect($removeButton).toHaveClass("selected-options__option-remove");
      expect($removeButton).toHaveAttribute("type", "button");
    }

    await user.click($removeButtons[0]);
    $ul = $container.querySelector("ul");
    $lis = $ul.querySelectorAll("li");
    expect($multiSelect.options[0].selected).toBeFalsy();
    expect($lis).toHaveLength(1);
    expect(onChangeSpy).toHaveBeenCalledTimes(1);

    await user.click($removeButtons[1]);
    $ul = $container.querySelector("ul");
    $lis = $ul.querySelectorAll("li");
    expect($multiSelect.options[2].selected).toBeFalsy();
    expect($lis).toHaveLength(0);
    expect(onChangeSpy).toHaveBeenCalledTimes(2);
  });
});
