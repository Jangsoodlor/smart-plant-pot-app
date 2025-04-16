import unittest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
import time
from random import randint
from selenium_singleton import Browser

def print_things(text):
    try: print(text.text)
    except Exception: print("skipped")
    
def find_in_list(_list, text): 
    for i in range(len(_list)):
        try:
            if _list[i].text == text:
                return i
        except Exception:
            continue
    return -1

class MainPageTest(unittest.TestCase):
    def setUp(self):
        self.driver = Browser.get_browser()
        self.page = 'http://localhost:8501/'
        self.driver.implicitly_wait(0.5)

    def test_validate_current_sensor_readings_is_working(self):
        self.driver.get(self.page)
        time.sleep(10)
        self.driver.implicitly_wait(10)
        heading = self.driver.find_elements(by=By.XPATH, value="//div[@data-testid='stMarkdownContainer']")
        # print(list(map(print_things, heading)))
        index = find_in_list(heading, "Current sensor readings")
        self.assertEqual("Current sensor readings", heading[index].text)
        self.assertIn("Last Updated", heading[index+1].text)
        
    def test_validate_current_weather_condition_is_working(self):
        self.driver.get(self.page)
        time.sleep(10)
        self.driver.implicitly_wait(10)
        heading = self.driver.find_elements(by=By.XPATH, value="//div[@data-testid='stMarkdownContainer']")
        # print(list(map(print_things, heading)))
        index = find_in_list(heading, "Current weather condition")
        self.assertEqual("Current weather condition", heading[index].text)
        self.assertIn("Last Updated", heading[index+1].text)
        
    def tearDown(self):
        self.driver.quit()
if __name__ == '__main__':
    unittest.main()