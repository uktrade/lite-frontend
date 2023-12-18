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

/**
 * @param {string} string The string to find the phrase in
 * @param {number} index The index to extract the current phrase from
 * @param {array[string]} patterns Patterns to use to create boundaries
 *
 * Given an index in a string will return the phrase that straddles that index.
 *
 * A phrase is defined by the boundaries given by the patterns
 *
 * Example:
 *   "foo This is our string bar"
 *   with patterns for "foo" and "bar"
 *   If we ask for the index in the following place
 *   "foo This is ou|r string bar" - this is essentially imagining where a text cursor would be
 *   This would return the phrase "This is our string"
 *
 * @returns {[string, number, number]} The found word and the indexes where it was found
 */
const getCurrentPhrase = (string, index, patterns) => {
  let startIndex = index;
  let endIndex = index;

  // If our index is in a pattern then we just return a basic return which is
  // equivalent to not being found
  for (const pattern of patterns) {
    if (isIndexInPattern(index, pattern, string)) {
      return ["", index, index];
    }
  }

  // First we check our index moving backwards to work out the start of our
  // phrase
  // We do this by finding the first index match of a pattern.
  let foundEnd = false;
  while (endIndex < string.length && !foundEnd) {
    endIndex += 1;
    for (const pattern of patterns) {
      if (isIndexInPattern(endIndex, pattern, string)) {
        foundEnd = true;
        break;
      }
    }
  }

  // Second we check our index moving forward to work out the end of our phrase
  // We do this by finding the first index match of a pattern.
  let foundStart = false;
  while (startIndex > 0 && !foundStart) {
    startIndex -= 1;
    for (const pattern of patterns) {
      if (isIndexInPattern(startIndex, pattern, string)) {
        foundStart = true;
        break;
      }
    }
  }

  // We now strip the phrase based on our found indexes
  let phrase = string.substring(startIndex, endIndex);

  // This then gives us a phrase with possible whitespace at the beginning and
  // end.
  // We then work out where the whitespace begins and ends and strip it out
  // accordingly whilst updating our found and end indexes to account for the
  // removed whitespace.
  const startWhitespaceLength = phrase.match(/^ */)[0].length;
  const endWhitespaceLength = phrase.match(/ *$/)[0].length;
  phrase = phrase.substring(
    startWhitespaceLength,
    phrase.length - endWhitespaceLength
  );
  startIndex += startWhitespaceLength;
  endIndex -= endWhitespaceLength;

  return [phrase, startIndex, endIndex];
};

export { getCurrentPhrase, getCurrentWord, isIndexInPattern };
