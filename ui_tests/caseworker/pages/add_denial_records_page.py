import csv
import glob
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ui_tests.caseworker.pages.BasePage import BasePage


class AddDenialRecordsPage(BasePage):
    CSV_FILE_LOCATION = "/tmp/example-denials.csv"

    def download_example_csv_file(self):
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.LINK_TEXT, "Download an example .csv file"))
        ).click()

        for _ in range(20):
            if os.path.exists(self.CSV_FILE_LOCATION):
                return
            time.sleep(0.2)

        raise AssertionError(f"CSV file failed to download to {self.CSV_FILE_LOCATION}")

    def update_example_csv_file(self, **fields):
        with open(self.CSV_FILE_LOCATION) as f:
            reader = csv.DictReader(f)
            first_row = next(reader)

        for name, value in fields.items():
            first_row[name] = value

        with open(self.CSV_FILE_LOCATION, "wt") as f:
            writer = csv.DictWriter(f, reader.fieldnames)
            writer.writeheader()
            writer.writerow(first_row)

    def upload_csv_file(self):
        self.driver.find_element(by=By.NAME, value="csv_file").send_keys(self.CSV_FILE_LOCATION)

    def get_banner_text(self):
        return self.driver.find_element(by=By.CLASS_NAME, value="app-snackbar__content").text

    def cleanup_temporary_files(self):
        """Cleans up files that match the following:

        /tmp/example-denials.csv
        /tmp/example-denials (1).csv
        /tmp/example-denials (2).csv
        ... etc ...
        """
        for file in [f for f in glob.glob(self.CSV_FILE_LOCATION.replace(".", "*."))]:
            try:
                os.remove(file)
            except OSError:
                pass
