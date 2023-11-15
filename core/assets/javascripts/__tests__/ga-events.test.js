import "@testing-library/jest-dom";
import { gaPushUserID, getUserID } from "../ga-events";

const createInputUserIDElement = () => {
  document.body.innerHTML = `
      <div>
        <input type="hidden" id="user_id" value="1234">
      </div>
    `;
  return document.querySelector("div");
};

const createEmptyElement = () => {
  document.body.innerHTML = `
    <div>
    </div>
  `;
  return document.querySelector("div");
};

describe("Hidden user_id input", () => {
  beforeEach(() => {
    createInputUserIDElement();
  });

  test("test getting user_id", async () => {
    let userID = getUserID();
    expect(userID).toBe("1234");
  });

  test("test pushing ga user_id no datalayer", async () => {
    expect(window.dataLayer).toBe(undefined);
    gaPushUserID();
    expect(window.dataLayer).toBe(undefined);
  });

  test("test pushing ga user_id with datalayer", async () => {
    expect(window.dataLayer).toBe(undefined);
    window.dataLayer = ["ga"];
    expect(window.dataLayer).toStrictEqual(["ga"]);
    gaPushUserID();
    // eslint-disable-next-line camelcase
    expect(window.dataLayer).toContainEqual({ user_id: "1234" });
  });

  test("test pushing ga user_id with no user_id with datalayer", async () => {
    createEmptyElement();
    window.dataLayer = ["ga"];
    gaPushUserID();
    expect(window.dataLayer).toStrictEqual(["ga"]);
  });
});
