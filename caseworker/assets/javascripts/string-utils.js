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

const replaceAtPosition = (string, replacement, startIndex, endIndex) => {
  const beginning = string.substring(0, startIndex);
  const ending = string.substring(endIndex, string.length);
  const newValue = `${beginning}${replacement}${ending}`;

  return [newValue, startIndex, startIndex + replacement.length];
};

export { getCurrentWord, isIndexInPattern, replaceAtPosition };
