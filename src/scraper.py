from time import sleep
from typing import List, Generator

from seleniumbase import Driver
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from tqdm.auto import tqdm
from functools import partial
from selenium.webdriver.chrome.options import Options

browser_options = Options()
browser_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
browser_options.add_argument('--incognito')
# Some websites block requests from headless browsers. Comment line and retry
browser_options.add_argument("--headless")  # Run browser in headless mode
browser_options.add_argument("--disable-gpu")  # Disable GPU acceleration
browser_options.add_argument("--no-sandbox")  # Bypass OS security model
browser_options.add_argument("--window-size=1280,720")  # Set window size if needed

def __check_console(driver, target):
    if not target:
        return True
    logs = driver.get_log("browser")
    for entry in logs:
        if target in entry["message"]:
            return True
    return False


def download_rendered_markup(
        urls: List[str],
        delay: int = 0,
        script: str = None,
        terminator_string:str=None,
        timeout:int=6000,
        solve_captcha: bool=False,
) -> Generator[str, None, None]:
    """
    Downloads and renders the markup of specified URLs using a browser driver.

    Supports executing JavaScript scripts on the loaded pages and handles both
    CAPTCHA-protected and non-CAPTCHA websites. The function allows for delay
    between page loads and customizable timeout for script execution.
    If the browser has to solvw a CAPTCHA, the headless mode will be disabled.

    Args:
        urls (List[str]): A list of URLs to fetch and render.
        delay (int): The delay, in seconds, to wait after opening a URL. Defaults to 0.
        script (str): JavaScript code to execute after page load. Optional.
        terminator_string (str): A string to wait for in the browser's console
            after executing the script. Optional.
        timeout (int): Maximum time, in milliseconds, to wait for script completion. Defaults to 6000.
        solve_captcha (bool): Specifies whether to handle CAPTCHA challenges. Defaults to False. Disables headless mode.

    Returns:
        Generator[Tuple[str, str]]: A generator yielding tuples where the first element
            is the URL and the second is the rendered HTML markup of the page.
    """
    def __execute_script(browser_):
        # Execute script
        browser_.execute_script(script)
        # Wait for it to finish
        WebDriverWait(browser_, timeout).until(
            partial(__check_console, target=terminator_string)
        )
        return browser_.page_source

    if solve_captcha:
        with Driver(uc=True, headless=False) as browser:
            for url in tqdm(urls):
                try:
                    # open URL using UC mode with 6 second reconnect time to bypass initial detection
                    browser.uc_open_with_reconnect(url, reconnect_time=6)
                    # attempt to click the CAPTCHA checkbox if present
                    browser.uc_gui_click_captcha()

                    # Grab markup
                    markup = browser.page_source
                    if script:
                        markup = __execute_script(browser)
                    yield markup
                except Exception as e:
                    print(e)
            # close the browser and end the session
            browser.quit()

    else:
            with Chrome(options=browser_options) as browser:
                for url in tqdm(urls):
                    # Open website
                    browser.get(url)
                    # Sleep for n seconds. Necessary for some slow websites
                    sleep(delay)
                    # Get initial markup
                    markup = browser.page_source
                    if script:
                        markup = __execute_script(browser)
                    yield markup
                browser.quit()
    return None


if __name__ == '__main__':
    pass