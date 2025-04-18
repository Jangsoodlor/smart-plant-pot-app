import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium_manager import Browser


def print_things(text):
    try:
        print(text.text)
        print(dir(text))
    except Exception:
        print("skipped")


def find_in_list(_list, text):
    for i in range(len(_list)):
        try:
            if _list[i].text == text:
                return i
        except Exception:
            continue
    return -1


class GraphPageTest(unittest.TestCase):
    WAIT_TIME = 5

    def setUp(self):
        self.driver = Browser.get_browser()
        self.page = "http://localhost:8501/graph"
        self.driver.implicitly_wait(0.5)

    def test_radio_button_is_working(self):
        self.driver.get(self.page)
        time.sleep(self.WAIT_TIME)
        self.driver.implicitly_wait(self.WAIT_TIME)
        button_names = self.driver.find_elements(
            by=By.XPATH, value="//div[@data-testid='stRadio']"
        )[0].text.split("\n")
        labels = self.driver.find_elements(
            by=By.XPATH, value="//label[@data-baseweb='radio']"
        )
        wait = WebDriverWait(self.driver, self.WAIT_TIME)
        for name_index in range(len(button_names)):
            button = wait.until(EC.element_to_be_clickable(labels[name_index]))
            button.click()
            time.sleep(5)
            text = self.driver.find_element(
                by=By.XPATH, value="//*[name()='text' and @class='ytitle']"
            )
            self.assertIn(button_names[name_index], text.text)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
