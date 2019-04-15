from selenium import webdriver
import os
import pytest


class TestSample():
    @pytest.fixture()
    def test_setup(self):
        project_root = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(project_root)
        print("dir:" + base_dir)
        chrome_driver_path = base_dir + "/drivers/chromedriver"

        global driver
        self.driver = webdriver.Chrome(chrome_driver_path)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # self.driver = webdriver.Chrome(options=chrome_options)
        # self.driver.implicitly_wait(10)

        yield
        self.driver.close()
        self.driver.quit()
        print("Test Complete")

    def test_login(self, test_setup):
            self.driver.get("https://lite-exporter-frontend-dev.london.cloudapps.digital/")
            x = self.driver.title
            assert x == 'Exporter Hub - LITE'
