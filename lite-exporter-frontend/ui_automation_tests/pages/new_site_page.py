from selenium.webdriver.common.keys import Keys


class NewSite:

    def __init__(self, driver):
        self.driver = driver
        self.name = driver.find_element_by_id("name")
        self.address_line_1 = driver.find_element_by_id("address.address_line_1")
        self.postcode = driver.find_element_by_id("address.postcode")
        self.city = driver.find_element_by_id("address.city")
        self.region = driver.find_element_by_id("address.region")
        self.country = driver.find_element_by_id("address.country")

    def enter_info_for_new_site(self, name, address, postcode, city, region, country):
        self.name.send_keys(name)
        self.address_line_1.send_keys(address)
        self.postcode.send_keys(postcode)
        self.city.send_keys(city)
        self.region.send_keys(region)
        self.country.send_keys(country)

    def clear_info_for_site(self):
        self.name.clear()
        self.address_line_1.clear()
        self.postcode.clear()
        self.city.clear()
        self.region.clear()

