module.exports = {
  // A list of paths to directories that Jest should use to search for files in
  roots: [
    "caseworker/assets/javascripts",
    "core/assets/javascripts",
  ],

  // The test environment that will be used for testing
  testEnvironment: "jsdom",

  "automock": false,

  "setupFiles": [
    "./setupJest.js"
  ]
};
