# for Python <3.9 use 'from typing import Collection'
from selenium import webdriver

authen_authorized_payment = [401, 402, 407, 511]

class Browser:
    """Provide access to an instance of a Selenium web driver.

    Methods:
    get_browser(cls)  class method that returns an instance of a WebDriver
    """
    _instance:webdriver.remote.webdriver.WebDriver|None  = None
    @classmethod
    def get_browser(cls) -> webdriver.remote.webdriver.WebDriver:
        if cls._instance is None:
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")        
            cls._instance = webdriver.Firefox(options=options)
        return cls._instance
