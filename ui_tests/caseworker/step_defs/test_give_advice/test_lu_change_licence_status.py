from pytest_bdd import scenarios
from pytest_bdd import scenarios


scenarios("../../features/give_advice/lu_licence_change_status.feature", strict_gherkin=False)


# Log out as current user
# Log in as a user with the role "Licensing Unit Senior Manager"
# Go to the "Cases" page
# Filter for the case with licence status "finalised"
# Click on the case
# Click on the "Change licence status" button
# Select the new licence status "suspended"
# Assert that it's visible in the UI
