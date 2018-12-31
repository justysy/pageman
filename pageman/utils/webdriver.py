import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


_DEBUG = False


# # path.getTotalLength
# def get_svg_path_total_length(element):
#     driver = element.parent
#     return driver.execute_script("return arguments[0].getTotalLength(arguments[1]);", element)
#
#
# # path.getPointAtLength
# def get_svg_path_point_at_length(element, length):
#     driver = element.parent
#     return driver.execute_script("return arguments[0].getPointAtLength(arguments[1]);", element, length)


def execute_js_on_browser(element, browser_js, *args):
    driver = element.parent
    return driver.execute_script(browser_js, element, *args)


def highlight_one(element, color='aquamarine'):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element.parent

    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)
    original_style = element.get_attribute('style')
    apply_style("background: {0}; border: 2px solid aqua;".format(color))
    time.sleep(.4)
    apply_style(original_style)


def highlight_all(elements, color='aquamarine'):
    """Highlights (blinks) Selenium Webdriver elements"""
    if len(elements) == 0:
        return
    driver = elements[0].parent
    original_styles = {}

    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)
    for element in elements:
        original_styles[str(element)] = element.get_attribute('style')
        apply_style("background: {0}; border: 2px solid aqua;".format(color))
    time.sleep(.2)
    for element in elements:
        apply_style(original_styles[str(element)])


def wait_element_presence(locator, root, timeout):
    global _DEBUG
    try:
        element = WebDriverWait(root, timeout).until(
            EC.presence_of_element_located(locator)
        )
    except TimeoutException:
        print locator
        # print root.get_attribute('class')
        # highlight_one(root._element, 'red')
        raise
    except StaleElementReferenceException:
        print locator
        # highlight_one(root._element, 'red')
        raise
    if _DEBUG:
        highlight_one(element)
    return element


def wait_element_clickable(locator, root, timeout):
    global _DEBUG
    try:
        element = WebDriverWait(root, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    except TimeoutException:
        print locator
        # print root.get_attribute('class')
        # highlight_one(root)
        raise
    if _DEBUG:
        highlight_one(element)
    return element


def wait_all_elements_presence(locator, root, timeout):
    global _DEBUG
    try:
        elements = WebDriverWait(root, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )
    except TimeoutException:
        print locator
        # print root.get_attribute('class')
        # highlight_one(root._element, 'red')
        raise
    except StaleElementReferenceException:
        print locator
        # highlight_one(root._element, 'red')
        raise
    if _DEBUG:
        highlight_all(elements)
    return elements


def reset_mouse_position(driver):
    mouse_to_location(driver, -1920, -1080)


def mouse_to_location(driver, x, y):
    actions = ActionChains(driver)
    actions.move_by_offset(xoffset=x, yoffset=y)
    actions.perform()


def mouse_to_element(driver, element, offset=None):
    actions = ActionChains(driver)
    if offset is None:
        # actions.move_to_element(element)
        size = element.size
        actions.move_to_element_with_offset(element, int(size['width']/2.), int(size['height']/2.))
        # actions.move_by_offset(xoffset=xoffset, yoffset=yoffset)
    else:
        x_offset, y_offset = offset
        actions.move_to_element_with_offset(element, x_offset, y_offset)
    actions.perform()


def set_debug(debug):
    global _DEBUG
    _DEBUG = debug


def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root
