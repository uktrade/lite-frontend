import { getByText } from "@testing-library/dom";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import { TableExpander } from "../table-expander";

const createTableElement = () => {
  document.body.innerHTML = `
    <table class="table-expander">
      <thead class="govuk-table__head">
        <tr class="govuk-table__row"><!-- Column headers here --></tr>
      </thead>
      <tbody class="table-expander__distinct-hits">
        <tr><!-- Distinct hits here --></tr>
      </tbody>
      <tbody class="table-expander__remaining-hits">
        <tr><!-- Remaining hits here --></tr>
      </tbody>
    </table>
  `;
  return document.querySelector(".table-expander");
};

const createComponent = () => {
  let table = createTableElement();
  new TableExpander(table).init();
  return table;
};

describe("Table Expander", () => {
  test("Initial state without JS has no link and shows remaining hits", () => {
    let table = createTableElement();

    const showMoreCasesTableBody = table.querySelector(
      ".table-expander__show-more-cases-table-body"
    );
    expect(showMoreCasesTableBody).not.toBeInTheDocument();

    const remainingHits = table.querySelector(
      ".table-expander__remaining-hits"
    );
    expect(remainingHits).not.toHaveClass(
      "table-expander__remaining-hits__hidden"
    );
  });

  test("Initial state with JS has link and hides remaining hits", () => {
    const table = createComponent();

    const showMoreCasesTableBody = table.querySelector(
      ".table-expander__show-more-cases-table-body"
    );
    expect(showMoreCasesTableBody).toBeInTheDocument();

    const remainingHits = table.querySelector(
      ".table-expander__remaining-hits"
    );
    expect(remainingHits).toHaveClass("table-expander__remaining-hits__hidden");
  });

  test("Clicking 'Show more' link reveals remaining hits and hides link", async () => {
    const table = createComponent();

    const showMoreLink = getByText(table, "+ Show more cases for this product");
    expect(showMoreLink).toBeInTheDocument();

    await userEvent.click(showMoreLink);

    const remainingHits = table.querySelector(
      ".table-expander__remaining-hits"
    );
    expect(remainingHits).not.toHaveClass(
      "table-expander__remaining-hits__hidden"
    );
    expect(showMoreLink).not.toBeInTheDocument();
  });
});
