from shared.BasePage import BasePage


class RespondToEcjuQueryPage(BasePage):
    RESPONSE_FORM = "response"  # ID

    def enter_form_response(
        self, value,
    ):
        response_tb = self.driver.find_element_by_id(self.RESPONSE_FORM)
        response_tb.clear()
        response_tb.send_keys(value)
