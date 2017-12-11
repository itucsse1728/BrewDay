import random
import string

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class Test(object):

    def __init__(self):
        self.site = 'http://127.0.0.1:8000'
        self.delay = 2  # seconds
        self.username = 'ismail2'
        self.email = 'ismail@ismail.com'
        self.password = 'namdar123'
        self.browser = None

    def check_sign_up(self):
        url = '/'

        self.browser.get(self.site + url)

        signup_input = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_element_by_xpath('//a[@name="pop-up-signup"]'))

        signup_input.click()

        popups = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="mfp-with-anim mfp-hide mfp-dialog clearfix"]'))

        username_input = popups[1].find_element_by_xpath('//input[@name="username"]')
        email_input = popups[1].find_element_by_xpath('//input[@name="email"]')
        password_input = popups[1].find_element_by_xpath('//input[@name="password"]')
        password2_input = popups[1].find_element_by_xpath('//input[@name="password2"]')
        checkbox_input = popups[1].find_element_by_xpath('//input[@class="i-check"]')

        signup_button = popups[1].find_element_by_xpath('//input[@name="sign-up"]')

        username_input.send_keys(self.username)
        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        password2_input.send_keys(self.password)
        checkbox_input.click()

        signup_button.click()

        assert True

    def check_sign_in(self):
        url = '/'

        self.browser.get(self.site + url)

        login_input = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_element_by_xpath('//a[@name="pop-up-login"]'))

        login_input.click()

        popup = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_element_by_xpath('//div[@class="mfp-with-anim mfp-hide mfp-dialog clearfix"]'))

        username_input = popup.find_element_by_xpath('//input[@name="username"]')
        password_input = popup.find_element_by_xpath('//input[@name="password"]')

    def check_login(self):
        url = '/admin'

        self.browser.get(self.site + url)

        user_input = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_element_by_xpath('//input[@name="username"]'))
        pass_input = self.browser.find_element_by_xpath('//input[@name="password"]')

        user_input.send_keys(self.username)
        pass_input.send_keys(self.password)

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
        self.browser = webdriver.Chrome('/Users/ismail/Downloads/chromedriver')

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
