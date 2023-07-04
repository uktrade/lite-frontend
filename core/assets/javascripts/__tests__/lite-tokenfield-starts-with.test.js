import LiteTokenFieldStartsWith from "../lite-tokenfield-starts-with";
// make a document with a basic dropdown to instantiate and filter with tokenfield

const createElements = () => {
  document.body.innerHTML = `
    <select
    name="mentions"
    aria-describedby="id_mentions_hint"
    class="selectmultiple"
    id="id_mentions"
    multiple=""
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

  const element = document.querySelector("#id_mentions");
  return element;
};

const createTokenField = (element, items) => {
  return new LiteTokenFieldStartsWith({
    el: element,
    items: items,
    newItems: false,
    addItemOnBlur: true,
    filterSetItems: false,
    addItemsOnPaste: true,
    minChars: 1,
    itemName: element.name,
    setItems: [],
    keepItemsOrder: false,
  });
};

describe("LiteTokenFieldStartsWith", () => {
  const items = [
    {
      id: "12345",
      name: "damien",
      class: [],
    },
    {
      id: "1234",
      name: "Daniel",
      class: [],
    },
    {
      id: "123",
      name: "adam",
      class: [],
    },
    {
      id: "678",
      name: "Mathew (DDAT)",
      class: [],
    },
  ];
  const element = createElements();
  const tokenField = createTokenField(element, items);

  test("_filterData a", () => {
    const expected = [
      {
        id: "123",
        name: "adam",
        class: [],
      },
      {
        id: "12345",
        name: "damien",
        class: [],
      },
      {
        id: "1234",
        name: "Daniel",
        class: [],
      },
      {
        id: "678",
        name: "Mathew (DDAT)",
        class: [],
      },
    ];
    let orderedItems = tokenField._filterData("a", items);
    expect(orderedItems).toStrictEqual(expected);
  });

  test("_filterData da", () => {
    const expected = [
      {
        id: "12345",
        name: "damien",
        class: [],
      },
      {
        id: "1234",
        name: "Daniel",
        class: [],
      },
      {
        id: "123",
        name: "adam",
        class: [],
      },
      {
        id: "678",
        name: "Mathew (DDAT)",
        class: [],
      },
    ];
    let orderedItems = tokenField._filterData("da", items);
    expect(orderedItems).toStrictEqual(expected);
  });

  test("_filterData am", () => {
    const expected = [
      {
        id: "123",
        name: "adam",
        class: [],
      },
      {
        id: "12345",
        name: "damien",
        class: [],
      },
    ];
    let orderedItems = tokenField._filterData("am", items);
    expect(orderedItems).toStrictEqual(expected);
  });

  test("_filterData ddat", () => {
    const expected = [
      {
        id: "678",
        name: "Mathew (DDAT)",
        class: [],
      },
    ];
    let orderedItems = tokenField._filterData("ddat", items);
    expect(orderedItems).toStrictEqual(expected);

    orderedItems = tokenField._filterData("DDAT", items);
    expect(orderedItems).toStrictEqual(expected);
  });
});
