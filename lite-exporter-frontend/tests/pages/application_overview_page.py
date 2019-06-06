class ApplicationOverviewPage():

    def __init__(self, driver):
        self.driver = driver
        self.sites_link = "a[href*='sites']"
        self.goods_link = "goods"
        self.end_user_link = "end_users"

    def click_sites_link(self):
        self.driver.find_element_by_css_selector(self.sites_link).click()

    def click_goods_link(self):
        self.driver.find_element_by_id(self.goods_link).click()

    def click_end_user_link(self):
        element = self.driver.find_element_by_id(self.end_user_link)
        self.driver.execute_script("arguments[0].click();", element)
