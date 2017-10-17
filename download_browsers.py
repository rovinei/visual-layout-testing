from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver
import unittest
import time
import os


class TestDownload(unittest.TestCase):
    def setUp(self):

        self.chrome_pref = dict()
        self.save_path = os.environ['DOWNLOAD_PATH'] or '/Users/kit/Downloads/'
        self.url = os.environ['DOWNLOAD_URL']
        self.chrome_pref.update({
            "profile.default_content_settings.popups": 0,
            "download.default_directory": self.save_path,
            "safebrowsing.enabled": True

        })
        self.chrome_opts = webdriver.ChromeOptions()
        self.chrome_opts.add_experimental_option('prefs', self.chrome_pref)
        self.chrome_opts.add_argument('--test-type')
        self.chrome_opts.add_argument('--disable-extensions')
        self.chrome_opts.add_argument('--safebrowsing-disable-download-protection')
        self.capabilities = DesiredCapabilities.CHROME.copy()
        self.capabilities['acceptSslCerts'] = True

        self.driver = webdriver.Chrome(chrome_options=self.chrome_opts, desired_capabilities=self.capabilities)

    def tearDown(self):
        self.driver.quit()

    def test_download_browsers(self):
        self.driver.get(self.url)
        page_result = ui.WebDriverWait(self.driver, 45).until(
            lambda driver: self.driver.find_element_by_class_name('row-gallery'))
        item_links = page_result.find_elements_by_css_selector('.row-gallery .item a')
        self.actions = ActionChains(self.driver)
        self.actions.reset_actions()
        main_window = self.driver.current_window_handle

        for link in item_links:

            time.sleep(2)
            self.actions.key_down(Keys.COMMAND).click(link).key_up(Keys.COMMAND).perform()
            time.sleep(15)
            self.driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(3)
            self.driver.find_element_by_tag_name('a').get_attribute()
            self.driver.close()
            self.driver.switch_to.window(main_window)
            self.actions.reset_actions()

        def check_download():
            max_mtime = 0
            newest_file = ''
            for filename in filter(os.path.isfile, os.listdir(self.save_path)):
                path = os.path.join(self.save_path, filename)
                try:
                    mtime = os.path.getmtime(path)
                    if mtime > max_mtime:
                        newest_file = path
                        max_mtime = mtime
                except OSError:
                    pass  # File probably just moved/deleted
            return newest_file

        time.sleep(5)
        download_file = check_download()

        while os.path.splitext(download_file)[1] == '.crdownload':
            print('downloading...')
            time.sleep(5)
            download_file = check_download()
            continue

        print('downloaded')


if __name__ == '__main__':
    unittest.main()

