import { getCurrentWord, replaceAtPosition } from "../string-utils";

describe("getCurrentWord", () => {
  test.each([
    ["foo", 0, ["foo", 0, 3]],
    ["foo", 1, ["foo", 0, 3]],
    ["foo", 2, ["foo", 0, 3]],
    ["foo", 3, ["foo", 0, 3]],
    ["foo bar", 4, ["bar", 4, 7]],
    ["foo bar", 5, ["bar", 4, 7]],
    ["foo bar", 6, ["bar", 4, 7]],
    ["foo bar", 7, ["bar", 4, 7]],
    ["foo bar baz", 4, ["bar", 4, 7]],
    ["foo bar baz", 5, ["bar", 4, 7]],
    ["foo bar baz", 6, ["bar", 4, 7]],
    ["foo bar baz", 7, ["bar", 4, 7]],
    ["", 0, ["", 0, 0]],
  ])("Retrieving current word", (string, index, expected) => {
    expect(getCurrentWord(string, index)).toEqual(expected);
  });
});

describe("replaceAtPosition", () => {
  test.each([
    ["xxx", "bar", 0, 3, ["bar", 0, 3]],
    ["xxx", "bar", 1, 1, ["xbarxx", 1, 4]],
    ["xxx", "bar", 1, 2, ["xbarx", 1, 4]],
  ])(
    "Retrieving current word",
    (string, replacement, startIndex, endIndex, expected) => {
      expect(
        replaceAtPosition(string, replacement, startIndex, endIndex)
      ).toEqual(expected);
    }
  );
});
