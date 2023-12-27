import "@testing-library/jest-dom";

import MultiSelector from "../multi-selector";

const createElements = () => {
  document.body.innerHTML = `
    <div id="container">
      <select id="select-multiple" multiple data-multi-select-objects-as-plural="objects">
        <option value="1">One</option>
        <option value="2">Two</option>
        <option value="3">Three</option>
      </select>
    </div>
  `;

  return [
    document.querySelector("#container"),
    document.querySelector("#select-multiple"),
  ];
};

describe("MultiSelector", () => {
  test("Configuring accessible autocomplete", () => {
    const mockAccessibleAutocomplete = jest.fn();
    const mockSelectedOptions = jest.fn().mockImplementation(() => {
      return { init: jest.fn() };
    });

    const [, $el] = createElements();

    new MultiSelector(
      mockAccessibleAutocomplete,
      mockSelectedOptions,
      $el
    ).init();

    const $wrapper = document.querySelector(".autocomplete__wrapper");

    const config = mockAccessibleAutocomplete.mock.calls[0][0];

    expect(config.id).toEqual("select-multiple");
    expect(config.autoselect).toEqual(true);
    expect(config.source).toEqual(["One", "Two", "Three"]);
    expect(config.displayMenu).toEqual("overlay");
    expect(config.element).toEqual($wrapper);
  });

  test("Renders autocomplete wrapper", () => {
    const mockAccessibleAutocomplete = jest.fn();
    const mockSelectedOptions = jest.fn().mockImplementation(() => {
      return { init: jest.fn() };
    });

    const [$container, $el] = createElements();

    new MultiSelector(
      mockAccessibleAutocomplete,
      mockSelectedOptions,
      $el
    ).init();

    const $wrapper = document.querySelector(".autocomplete__wrapper");
    expect($container).toContainElement($wrapper);
  });

  test("Sets new id for select", () => {
    const mockAccessibleAutocomplete = jest.fn();
    const mockSelectedOptions = jest.fn().mockImplementation(() => {
      return { init: jest.fn() };
    });

    const [, $el] = createElements();

    new MultiSelector(
      mockAccessibleAutocomplete,
      mockSelectedOptions,
      $el
    ).init();

    expect($el).toHaveAttribute("id", "select-multiple-select");
  });

  test("onConfirm selects options", () => {
    const mockAccessibleAutocomplete = jest.fn();
    const mockSelectedOptions = jest.fn().mockImplementation(() => {
      return { init: jest.fn() };
    });

    const [, $el] = createElements();

    const onChangeSpy = jest.fn();
    $el.addEventListener("change", () => onChangeSpy());

    new MultiSelector(
      mockAccessibleAutocomplete,
      mockSelectedOptions,
      $el
    ).init();

    expect(onChangeSpy).toBeCalledTimes(0);
    expect($el.selectedOptions).toHaveLength(0);

    const config = mockAccessibleAutocomplete.mock.calls[0][0];

    config.onConfirm("One");
    expect($el.options[0].selected).toBeTruthy();
    expect(onChangeSpy).toBeCalledTimes(1);

    config.onConfirm("Three");
    expect($el.options[2].selected).toBeTruthy();
    expect(onChangeSpy).toBeCalledTimes(2);
  });

  test("onConfirm clears accessible input", () => {
    jest.useFakeTimers();

    const [$container, $el] = createElements();

    let $input;
    const mockAccessibleAutocomplete = jest.fn(() => {
      $input = document.createElement("input");
      $input.type = "text";
      $input.id = "select-multiple";
      $container.appendChild($input);
    });
    const mockSelectedOptions = jest.fn().mockImplementation(() => {
      return { init: jest.fn() };
    });

    const onChangeSpy = jest.fn();
    $el.addEventListener("change", () => onChangeSpy());

    new MultiSelector(
      mockAccessibleAutocomplete,
      mockSelectedOptions,
      $el
    ).init();

    const config = mockAccessibleAutocomplete.mock.calls[0][0];

    $input.value = "One";
    config.onConfirm("One");
    expect($input).toHaveValue("One");
    jest.runAllTimers();
    expect($input).toHaveValue("");

    $input.value = "Three";
    config.onConfirm("Three");
    expect($input).toHaveValue("Three");
    jest.runAllTimers();
    expect($input).toHaveValue("");

    jest.useRealTimers();
  });

  test("Configuring select options", () => {
    const mockAccessibleAutocomplete = jest.fn();
    const mockSelectedOptions = jest.fn().mockImplementation(() => {
      return { init: jest.fn() };
    });

    const [$container, $el] = createElements();

    new MultiSelector(
      mockAccessibleAutocomplete,
      mockSelectedOptions,
      $el
    ).init();

    const [optionsWrapperParam, elParam, pluralParam] =
      mockSelectedOptions.mock.calls[0];

    expect(optionsWrapperParam).toEqual(
      $container.querySelector(".multi-select__selected-options-wrapper")
    );
    expect(elParam).toEqual($el);
    expect(pluralParam).toEqual("objects");
  });

  test("Sets multi select display to none", () => {
    const mockAccessibleAutocomplete = jest.fn();
    const mockSelectedOptions = jest.fn().mockImplementation(() => {
      return { init: jest.fn() };
    });

    const [, $el] = createElements();

    new MultiSelector(
      mockAccessibleAutocomplete,
      mockSelectedOptions,
      $el
    ).init();

    expect($el).not.toBeVisible();
  });
});
