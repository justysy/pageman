import os
import contextlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities


def main():
    user_home = os.path.expanduser('~')
    driver_bin = os.path.join(user_home, 'chrome_driver', 'chromedriver')
    print(driver_bin)
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')

    url = 'https://www.google.com.tw/maps/'

    with contextlib.closing(webdriver.Chrome(executable_path=driver_bin, chrome_options=chrome_options)) as driver:
        driver.get(url=url)


if __name__ == '__main__':
    main()
