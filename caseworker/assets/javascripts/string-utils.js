/**
 * @param {string} string The string to find the word in
 * @param {number} index The index to extract the current word
 *
 * Given an index in a string will return the word that straddles that index.
 *
 * Example:
 *   "This is our string"
 *   If we ask for the index in the following place
 *   "This is ou|r string" - this is essentially imagining where a text cursor would be
 *   This would return the word "our"
 *
 * @returns {[string, number, number]} The found word and the indexes where it was found
 */
const getCurrentWord = (string, index) => {
  let startIndex = index;
  let endIndex = index;

  while (endIndex < string.length) {
    endIndex += 1;
    const word = string.substring(startIndex, endIndex);
    if (word.at(-1) === " ") {
      endIndex -= 1;
      break;
    }
  }

  while (startIndex > 0) {
    startIndex -= 1;
    const word = string.substring(startIndex, endIndex);
    if (word.at(0) === " ") {
      startIndex += 1;
      break;
    }
  }

  const word = string.substring(startIndex, endIndex);
  return [word, startIndex, endIndex];
};

/**
 * @param {number} index The index to check whether it sits in a matched pattern
 * @param {string} pattern The pattern to match on
 * @param {string} string The string to match the pattern in
 *
 * Will check whether the specified string index falls within the indexes of a
 * match from the desired pattern.
 *
 * @returns {boolean} Whether the index is in a pattern match
 */
const isIndexInPattern = (index, pattern, string) => {
  for (const match of string.matchAll(RegExp(pattern, "dg"))) {
    const [startIndex, endIndex] = match.indices[0];
    if (index < startIndex) {
      return false;
    }
    if (index >= startIndex && index <= endIndex) {
      return true;
    }
  }

  return false;
};

export { getCurrentWord, isIndexInPattern };
