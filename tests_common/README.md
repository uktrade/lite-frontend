# lite-tests-common
###This project can be used and expanded upon as a stand-alone service.

To seed the database with `X` amount of cases:
 1. `pipenv shell` whilst in the project's root
 2. `cd ..` to the directory where the project is held
 3. `python -m lite-tests-common.tools.seed_cases X` 
 
 If this project is a sub-project, the command can be used from the root of the parent project:
 1. `cd` to the directory where the project is held
 2. `pipenv run python -m <path.from.root.of.parent.project>.tools.seed_cases X` 
