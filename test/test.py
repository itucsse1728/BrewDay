import random
import string

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class Test(object):
    def __init__(self):
        self.site = 'http://127.0.0.1:8000'
        self.delay = 2  # seconds

        self.browser = None

    def check_login(self):
        url = '/admin'

        username = 'test'
        password = '123456gs'

        self.browser.get(self.site + url)

        user_input = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_element_by_xpath('//input[@name="username"]'))
        pass_input = self.browser.find_element_by_xpath('//input[@name="password"]')

        user_input.send_keys(username)
        pass_input.send_keys(password)

        pass_input.submit()

        WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_element_by_xpath('//div[@id="user-tools"]'))

    def check_brew(self):
        url = '/brew'

        self.browser.get(self.site + url)

        products = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="product"]'))

        product = random.choice(products)

        rate_form = product.find_element_by_tag_name('form')
        form_id = rate_form.get_attribute('id')

        list_items = rate_form.find_elements_by_tag_name('li')
        random_rate = random.randint(1, 5)

        list_items[random_rate-1].click()

        rate_form = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_element_by_xpath(f'//form[@id="{form_id}"]'))

        current_rate = 0
        list_items = rate_form.find_elements_by_tag_name('li')

        for item in list_items:
            a = item.find_element_by_tag_name('a')
            current_rate += a.get_attribute('style').strip().endswith('orange;')

        assert random_rate == current_rate

        products = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="product"]'))

        product = random.choice(products)

        textarea = product.find_element_by_tag_name('textarea')
        button = product.find_element_by_tag_name('button')

        textname = textarea.get_attribute('name')
        random_comment = ''.join(random.sample(string.printable, 10))

        textarea.clear()
        textarea.send_keys(random_comment)

        button.click()

        textarea = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_element_by_xpath(f'//textarea[@name="{textname}"]'))

        assert textarea.text == random_comment

    def run(self):
        self.browser = webdriver.Firefox()

        for attr in __class__.__dict__:
            if callable(getattr(self, attr)) and attr.startswith('check'):
                try:
                    getattr(self, attr)()
                    print(f"[+] {attr} passed")

                except Exception as e:
                    print(f"[-] {attr} failed")
                    print(e)

        self.browser.close()

if __name__ == '__main__':
    test = Test()
    test.run()