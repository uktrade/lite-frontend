import { getByText } from "@testing-library/dom";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import { TableExpander } from "../table-expander";

const createTableElement = () => {
  document.body.innerHTML = `
    <table class="table-expander">
      <thead>
        <tr><!-- Column headers here --></tr>
      </thead>
      <tbody>
        <tr><!-- Distinct hits here --></tr>
      </tbody>
      <tbody class="table-expander__show-more-cases-table-body">
        <tr><td><a href="#" class="table-expander__show-more-cases-link">Show More</a></td></tr>
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
  test("Initial state hides the table body and remaining hits", () => {
    const table = createComponent();

    const tableBody = table.querySelector(
      ".table-expander__show-more-cases-table-body"
    );
    expect(tableBody).toBeInTheDocument();

    const remainingHits = table.querySelector(
      ".table-expander__remaining-hits"
    );
    expect(remainingHits).toHaveClass("table-expander__remaining-hits__hidden");
  });

  test("Clicking 'Show More' link reveals remaining hits and hides link", async () => {
    const table = createComponent();

    const showMoreLink = getByText(table, "Show More");
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
