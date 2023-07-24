module.exports = {
    env: {
        browser: true,
        es2021: true,
        "jest/globals": true,
        jquery: true,
    },
    globals: {
        tippy: "readonly",
    },
    extends: "eslint:recommended",
    plugins: ["jest"],
    overrides: [
        {
            env: {
                node: true,
            },
            files: [".eslintrc.{js,cjs}"],
            parserOptions: {
                sourceType: "script",
            },
        },
    ],
    parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
    },
    rules: {
        "linebreak-style": ["error", "unix"],
        semi: ["error", "always"],
        "no-var": ["error"],
        camelcase: ["error", { properties: "always" }],
    },
};
