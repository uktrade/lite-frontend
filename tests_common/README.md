# lite-tests-common

### This project can be used and expanded upon as a stand-alone service.

To seed the database with `X` amount of cases:
1. create a `.env` file in the project's root (the required variables can be found in `local.env`)
2. `pipenv install` whilst in the project's root
3. `pipenv shell` whilst in the project's root
4. `cd ..` to the directory where the project is held
5. `python -m lite-tests-common.performance_testing.setup.seed_cases X`

 If this project is a submodule, the command can be used from the root of the parent project:
 1. `cd` to the directory where the project is held
 2. `pipenv run python -m <path.from.root.of.parent.project>.performance_testing.setup.seed_cases X`
