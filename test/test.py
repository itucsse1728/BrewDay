import time
import random
import string

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class Test(object):
    def __init__(self):
        self.site = 'http://127.0.0.1:8000'
        self.delay = 2  # seconds

        self.browser = None

        self.username = f'keo-{random.randint(1000, 9999)}'
        self.email = 'keo@keo.com'
        self.password = '123456gs'
        self.ingredient_name = ""
        self.ingredient_amount = '54.2'
        self.recipe_name = f'NEW RECIPE #{random.randint(1000, 9999)}'

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

        signup_button = popups[1].find_element_by_xpath('//input[@name="sign-up"]')

        username_input.send_keys(self.username)
        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        password2_input.send_keys(self.password)

        signup_button.click()

        assert (self.browser.find_element_by_xpath('//a[@name="navbar-name"]').text == self.username)

        self.browser.find_element_by_xpath('//a[@name="navbar-logout"]').click()

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
        login_input = popup.find_element_by_xpath('//input[@name="pop-up-login-button"]')

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)

        login_input.click()

        assert (self.browser.find_element_by_xpath('//a[@name="navbar-name"]').text == self.username)

    def check_profile(self):
        url = '/profile'
        self.browser.get(self.site + url)

        products = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="product"]'))

        product = products[0]

        name = product.find_element_by_tag_name('h4')
        email = product.find_element_by_tag_name('p')

        assert name.text == self.username and email.text == self.email

        product = products[1]

        ingredient = product.find_element_by_tag_name('td')
        self.ingredient_name = ingredient.text

        product.find_element_by_tag_name('button').click()
        time.sleep(0.3)

        products = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="product"]'))

        product = products[1]

        ingredients = product.find_elements_by_tag_name('td')

        for ingredient in ingredients:
            if ingredient.text == self.ingredient_name:
                assert False

        new_name = product.find_element_by_xpath('//input[@name="new-ingredient-name"]')
        new_amount = product.find_element_by_xpath('//input[@name="new-ingredient-amount"]')

        new_name.send_keys(self.ingredient_name)
        new_amount.send_keys(self.ingredient_amount)

        button = product.find_element_by_xpath('//button[@name="submit"]')
        button.click()
        time.sleep(0.3)

        product = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="product"]'))[1]

        rows = product.find_elements_by_tag_name('tr')
        flag = False

        for row in rows[:-1]:
            cols = row.find_elements_by_tag_name('td')

            try:
                current_amount = cols[1].find_element_by_tag_name('input').get_attribute('placeholder')

                if len(cols) == 3 and cols[0].text == self.ingredient_name and current_amount == self.ingredient_amount:
                    flag = True
                    break
            except:
                pass

        assert flag

    def check_add_recipe(self):
        url = '/recipe'

        self.browser.get(self.site + url)

        product = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_element_by_xpath('//div[@class="product"]'))

        recipe_name_input = product.find_element_by_xpath('//input[@name="recipeName"]')
        new_name_input = product.find_element_by_xpath('//input[@name="new-ingredient-name"]')
        new_amount_input = product.find_element_by_xpath('//input[@name="new-ingredient-amount"]')
        create_button = product.find_element_by_xpath('//button[@name="submit"]')

        recipe_name_input.send_keys(self.recipe_name)
        new_name_input.send_keys(self.ingredient_name)
        new_amount_input.send_keys(str(float(self.ingredient_amount) - 40))

        create_button.click()
        time.sleep(0.3)

        product = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="product"]'))[-1]

        assert product.find_element_by_xpath('.//ul[@class="product-labels"]').text.strip() == self.recipe_name

    def check_create_brew(self):
        url = '/recipe'
        self.browser.get(self.site + url)

        products = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="product"]'))

        product = None

        for p in products:
            p_name = p.find_element_by_xpath('.//ul[@class="product-labels"]').text.strip()
            if p_name == self.recipe_name:
                product = p

        assert product

        brew_button = product.find_element_by_xpath('.//button[@name="brew"]')
        brew_button.click()
        time.sleep(0.3)

        url = '/brew'
        self.browser.get(self.site + url)

        products = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="product"]'))

        flag = False
        for p in products:
            p_name = p.find_element_by_xpath('.//ul[@class="product-labels"]').text.strip()
            if p_name == self.recipe_name:
                flag = True
                break

        assert flag


    def check_rate_brew(self):
        url = '/brew'
        self.browser.get(self.site + url)

        products = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="product"]'))

        product = random.choice(products)

        rate_form = product.find_element_by_tag_name('form')
        form_id = rate_form.get_attribute('id')

        list_items = rate_form.find_elements_by_tag_name('li')
        random_rate = random.randint(1, 5)

        list_items[random_rate - 1].click()

        rate_form = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_element_by_xpath(f'//form[@id="{form_id}"]'))

        current_rate = 0
        list_items = rate_form.find_elements_by_tag_name('li')

        for item in list_items:
            a = item.find_element_by_tag_name('a')
            current_rate += a.get_attribute('style').strip().endswith('orange;')

        assert random_rate == current_rate

    def check_comment_brew(self):
        url = '/brew'
        self.browser.get(self.site + url)

        products = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="product"]'))

        product = random.choice(products)

        textarea = product.find_element_by_tag_name('textarea')
        button = product.find_element_by_tag_name('button')

        textname = textarea.get_attribute('name')
        random_comment = ''.join(random.sample(string.ascii_lowercase * 10, 10))

        textarea.clear()
        textarea.send_keys(random_comment)

        button.click()

        textarea = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_element_by_xpath(f'//textarea[@name="{textname}"]'))

        assert textarea.text == random_comment

    def check_delete_recipe(self):
        url = '/recipe'
        self.browser.get(self.site + url)

        products = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="product"]'))

        product = None

        for p in products:
            p_name = p.find_element_by_xpath('.//ul[@class="product-labels"]').text.strip()
            if p_name == self.recipe_name:
                product = p

        assert product

        delete_button = product.find_element_by_xpath('.//button[@name="delete"]')
        delete_button.click()
        time.sleep(0.3)

        products = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="product"]'))

        for p in products:
            p_name = p.find_element_by_xpath('.//ul[@class="product-labels"]').text.strip()
            if p_name == self.recipe_name:
                assert False

    def check_recommendation(self):
        self.browser.get(self.site + '/recommendation')

        product = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_element_by_xpath('//div[@class="product"]'))

        tbody = product.find_element_by_xpath('.//table/tbody')

        ingredients = {}

        for row in tbody.find_elements_by_xpath('./tr'):
            name, amount = row.find_elements_by_tag_name('td')
            name, amount = name.text, amount.text
            ingredients[name] = float(amount)

        button = self.browser.find_element_by_xpath('//button[@name="submit"]')

        button.click()

        products = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="product"]'))

        recipes = products[2:]

        for recipe in recipes:
            tbody = recipe.find_element_by_xpath('.//table/tbody')

            for row in tbody.find_elements_by_tag_name('tr'):
                name, amount = row.find_elements_by_tag_name('td')
                name, amount = name.text, float(amount.text)

                if amount and name not in ingredients:
                    raise ValueError('invalid recommendation')

                elif name in ingredients and amount > ingredients[name]:
                    raise ValueError('Invalid amount for {} : {} > {}'.format(name, amount, ingredients[name]))

    def run(self):
        self.browser = webdriver.Chrome(r'C:\Users\msi-nb\Documents\selenium\chromedriver.exe')

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