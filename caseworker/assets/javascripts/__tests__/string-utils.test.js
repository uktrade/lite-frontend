import {
  getCurrentPhrase,
  getCurrentWord,
  isIndexInPattern,
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

describe("getCurrentPhrase", () => {
  test.each([
    ["foo", 3, [], ["foo", 0, 3]],
    ["foo bar foo", 7, ["foo"], ["bar", 4, 7]],
    ["foo bar bar foo", 11, ["foo"], ["bar bar", 4, 11]],
    ["foo bar bar baz", 11, ["foo", "baz"], ["bar bar", 4, 11]],
    ["foo bar bar baz", 4, ["foo", "baz"], ["bar bar", 4, 11]],
    ["foo bar bar baz", 5, ["foo", "baz"], ["bar bar", 4, 11]],
    ["foo bar bar baz", 6, ["foo", "baz"], ["bar bar", 4, 11]],
    ["foo bar bar baz", 7, ["foo", "baz"], ["bar bar", 4, 11]],
    ["foo bar bar baz", 8, ["foo", "baz"], ["bar bar", 4, 11]],
    ["foo bar bar baz", 9, ["foo", "baz"], ["bar bar", 4, 11]],
    ["foo bar bar baz", 10, ["foo", "baz"], ["bar bar", 4, 11]],
    ["foo bar bar baz", 0, ["foo", "baz"], ["", 0, 0]],
    ["foo bar bar baz", 15, ["foo", "baz"], ["", 15, 15]],
    ["foo  bar bar  baz", 10, ["foo", "baz"], ["bar bar", 5, 12]],
  ])("Retrieving current phrase", (string, index, patterns, expected) => {
    expect(getCurrentPhrase(string, index, patterns)).toEqual(expected);
  });
});
