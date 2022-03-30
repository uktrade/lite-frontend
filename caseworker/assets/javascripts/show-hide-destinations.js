// Hide show destinations list.

const MAX_COUNTRIES_TO_DISPLAY = 3;

const hideItems = (countries) =>
  countries.forEach((country, index) => {
    if (index > MAX_COUNTRIES_TO_DISPLAY - 1) {
      country.classList.add("app-hidden--force");
    }
  });

const initDestinationsList = () => {
  const destinationsList = document.querySelectorAll(".destinations__list");

  destinationsList.forEach((destinations) => {
    const items = destinations.querySelectorAll("li");

    if (items.length <= MAX_COUNTRIES_TO_DISPLAY) {
      return;
    }

    hideItems(items);
    let hidden = true;

    const td = destinations.parentElement;
    const button = document.createElement("button");
    button.className = "lite-button--link";
    button.innerText = `View all (${items.length})`;
    td.appendChild(button);

    button.addEventListener("click", (e) => {
      e.preventDefault();

      if (hidden) {
        items.forEach((item) => item.classList.remove("app-hidden--force"));
        hidden = false;
        button.innerText = "View less";
      } else {
        hideItems(items);
        hidden = true;
        button.innerText = `View all (${items.length})`;
      }
    });
  });
};

export default initDestinationsList;
