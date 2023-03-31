import { fireEvent, getByText, waitFor } from "@testing-library/dom";
import userEvent from "@testing-library/user-event";
import "@testing-library/jest-dom";
import fetchMock from "jest-fetch-mock";

import { initAutocompleteField } from "../ars";

let testContainer, fieldElement, autoCompleteElement, getDefaultValueSpy;

const createElements = () => {
  document.body.innerHTML = `
    <div id="test-container">
        <input id="report_summary_field" type="text" name="report_summary_field_name"></input>
    </div>
  `;

  return [
    document.querySelector("#test-container"),
    document.querySelector("#report_summary_field"),
  ];
};

const createComponent = () => {
  getDefaultValueSpy = jest.fn();
  getDefaultValueSpy.mockReturnValue("default-value");
  [testContainer, fieldElement] = createElements();
  initAutocompleteField("field", "field_plural", getDefaultValueSpy);
  autoCompleteElement = document.querySelector("#_report_summary_field");
};

describe("ARS autocomplete", () => {
  beforeEach(() => {
    createComponent();
  });

  test("Creates container element", () => {
    const fieldContainer = document.querySelector(
      "#report_summary_field_container"
    );
    expect(testContainer).toContainElement(fieldContainer);
  });

  test("Autocomplete element exists", () => {
    const fieldContainer = document.querySelector(
      "#report_summary_field_container"
    );
    expect(fieldContainer).toContainElement(autoCompleteElement);
  });

  test("Hides original input", () => {
    expect(fieldElement).toHaveStyle({ display: "none" });
  });

  test("Default value is called and used", () => {
    expect(getDefaultValueSpy).toBeCalledWith(fieldElement);
    expect(autoCompleteElement).toHaveValue("default-value");
  });

  test("Calls endpoint when typing", async () => {
    jest.useFakeTimers();
    const user = userEvent.setup({ advanceTimers: jest.advanceTimersByTime });
    fetchMock.mockResponse(
      JSON.stringify({
        report_summary_field_plural: [{ id: "1", name: "test-1" }],
      })
    );
    await user.type(autoCompleteElement, "t");
    jest.runOnlyPendingTimers();
    expect(fetchMock).toBeCalledWith("/tau/report_summary/field?name=t");
  });

  test("Displays results", async () => {
    jest.useFakeTimers();
    const user = userEvent.setup({ advanceTimers: jest.advanceTimersByTime });
    fetchMock.mockResponse(
      JSON.stringify({
        report_summary_field_plural: [
          { id: "1", name: "test-1" },
          { id: "2", name: "test-2" },
        ],
      })
    );
    await user.type(autoCompleteElement, "t");
    jest.runOnlyPendingTimers();
    await waitFor(() => {
      const options = document.querySelector("#_report_summary_field__listbox");
      expect(getByText(options, "test-1")).toBeVisible();
      expect(getByText(options, "test-2")).toBeVisible();
    });
  });

  test("Select result", async () => {
    jest.useFakeTimers();
    const user = userEvent.setup({ advanceTimers: jest.advanceTimersByTime });
    fetchMock.mockResponse(
      JSON.stringify({
        report_summary_field_plural: [
          { id: "id-1", name: "test-1" },
          { id: "id-2", name: "test-2" },
        ],
      })
    );
    await user.type(autoCompleteElement, "t");
    jest.runOnlyPendingTimers();
    await waitFor(() => {
      const options = document.querySelector("#_report_summary_field__listbox");
      expect(getByText(options, "test-1")).toBeVisible();
      expect(getByText(options, "test-2")).toBeVisible();
    });
    const options = document.querySelector("#_report_summary_field__listbox");
    const optionToSelect = getByText(options, "test-1");
    await user.click(optionToSelect);
    expect(autoCompleteElement).toHaveValue("test-1")
    expect(fieldElement).toHaveValue("id-1");
  });

  test("Select and clear result", async () => {
    jest.useFakeTimers();
    const user = userEvent.setup({ advanceTimers: jest.advanceTimersByTime });
    fetchMock.mockResponse(
      JSON.stringify({
        report_summary_field_plural: [
          { id: "id-1", name: "test-1" },
          { id: "id-2", name: "test-2" },
        ],
      })
    );
    await user.type(autoCompleteElement, "t");
    jest.runOnlyPendingTimers();
    await waitFor(() => {
      const options = document.querySelector("#_report_summary_field__listbox");
      expect(getByText(options, "test-1")).toBeVisible();
      expect(getByText(options, "test-2")).toBeVisible();
    });
    const options = document.querySelector("#_report_summary_field__listbox");
    const optionToSelect = getByText(options, "test-1");
    await user.click(optionToSelect);
    expect(fieldElement).toHaveValue("id-1");
    await user.clear(autoCompleteElement);
    fireEvent.blur(autoCompleteElement);
    expect(autoCompleteElement).toHaveValue("");
    expect(fieldElement).toHaveValue("");
  });

  test("Select and blur without clearing", async () => {
    jest.useFakeTimers();
    const user = userEvent.setup({ advanceTimers: jest.advanceTimersByTime });
    fetchMock.mockResponse(
      JSON.stringify({
        report_summary_field_plural: [
          { id: "id-1", name: "test-1" },
          { id: "id-2", name: "test-2" },
        ],
      })
    );
    await user.type(autoCompleteElement, "t");
    jest.runOnlyPendingTimers();
    await waitFor(() => {
      const options = document.querySelector("#_report_summary_field__listbox");
      expect(getByText(options, "test-1")).toBeVisible();
      expect(getByText(options, "test-2")).toBeVisible();
    });
    const options = document.querySelector("#_report_summary_field__listbox");
    const optionToSelect = getByText(options, "test-1");
    await user.click(optionToSelect);
    expect(autoCompleteElement).toHaveValue("test-1");
    expect(fieldElement).toHaveValue("id-1");
    await user.click(autoCompleteElement);
    fireEvent.blur(autoCompleteElement);
    expect(autoCompleteElement).toHaveValue("test-1");
    expect(fieldElement).toHaveValue("id-1");
  });
});
