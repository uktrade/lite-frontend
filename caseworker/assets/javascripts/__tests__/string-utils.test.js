import {
  getCurrentWord,
  isIndexInPattern,
  replaceAtPosition,
} from "../string-utils";

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

describe("isIndexInPattern", () => {
  test.each([
    [0, "foo", "foo bar", true],
    [1, "foo", "foo bar", true],
    [2, "foo", "foo bar", true],
    [3, "foo", "foo bar", true],
    [4, "foo", "foo bar", false],
    [5, "foo", "foo bar", false],
    [6, "foo", "foo bar", false],
    [7, "foo", "foo bar", false],
    [0, "foo", "foo foo", true],
    [1, "foo", "foo foo", true],
    [2, "foo", "foo foo", true],
    [3, "foo", "foo foo", true],
    [4, "foo", "foo foo", true],
    [5, "foo", "foo foo", true],
    [6, "foo", "foo foo", true],
    [7, "foo", "foo foo", true],
    [0, "bar", "foo bar", false],
    [1, "bar", "foo bar", false],
    [2, "bar", "foo bar", false],
    [3, "bar", "foo bar", false],
    [4, "bar", "foo bar", true],
    [5, "bar", "foo bar", true],
    [6, "bar", "foo bar", true],
    [7, "bar", "foo bar", true],
  ])("Index in pattern", (index, pattern, string, expected) => {
    expect(isIndexInPattern(index, pattern, string)).toEqual(expected);
  });
});
