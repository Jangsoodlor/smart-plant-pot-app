from selenium import webdriver

class Browser:
    """Provide access to an instance of a Selenium web driver.

    Methods:
    get_browser(cls)  class method that returns an instance of a WebDriver
    """
    @classmethod
    def get_browser(cls) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        return webdriver.Chrome(options=options)