import unittest
from automation_ui_tests.tests.test_register_business import RegisterBusinessTest
from automation_ui_tests.tests.test_manage_cases import ManageCasesTest

# get all tests from SearchText and HomePageTest class
register_business_test = unittest.TestLoader().loadTestsFromTestCase(RegisterBusinessTest)
manage_cases_test = unittest.TestLoader().loadTestsFromTestCase(ManageCasesTest)

# create a test suite combining search_text and home_page_test
test_suite = unittest.TestSuite([register_business_test, manage_cases_test])

# run the suite
unittest.TextTestRunner(verbosity=2).run(test_suite)