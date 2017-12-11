from django.test import TestCase
from .models import Recipe, Ingredient, User, Brew
from .views import INGREDIENTS

class TestRecommendation(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='dummy',
                                             email='dummy@dmail.com',
                                             password='123')

        self.user2 = User.objects.create_user(username='dummy1',
                                              email='dummy@dmaik.com',
                                              password='123')

        Ingredient.init_ingredients(self.user2, INGREDIENTS)
        Ingredient.init_ingredients(self.user, INGREDIENTS)

        Ingredient.objects.filter(user=self.user).update(amount=5)

        self.recipe = Recipe.objects.create(name='recipe1',
                                            user=self.user,
                                            batch_size=123)

        for i, ingredient in enumerate(INGREDIENTS):
            Ingredient.objects.create(name=ingredient,
                                      amount= (i%2)*5,
                                      recipe=self.recipe)

        self.recipe2 = Recipe.objects.create(name='recipe2',
                                             user=self.user,
                                             batch_size=123)

        for i, ingredient in enumerate(INGREDIENTS):
            Ingredient.objects.create(name=ingredient,
                                      amount=10,
                                      recipe=self.recipe2)

        self.recipe3 = Recipe.objects.create(name='recipe3',
                                             user=self.user,
                                             batch_size=1234)

        Ingredient.init_ingredients(self.recipe3, INGREDIENTS)

    def test_recomm(self):
        self.client.force_login(self.user)
        response = self.client.post('/recommendation/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['recipes']), 2)


class TestProfile(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='dummy@dmail.com',
                                             email='dummy@dmail.com',
                                             password='123')
        self.ingredients = self.user.ingredient_set.create(name='Salt',
                                                           amount=14.0)

    def test_ingredient(self):

        self.client.force_login(self.user)
        response = self.client.post('/profile/', {self.ingredients.name: 122.0})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user.ingredient_set.get(name = self.ingredients.name).amount, 122.0)

    def test_user(self):

        self.client.force_login(self.user)
        response = self.client.get('/profile/')

        self.assertEqual(response.context["request"].user, self.user)


class TestBrew(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user-1', email='dummy@dmail.com', password='123')
        self.user2 = User.objects.create_user(username='user-2', email='dummy@dmail.com', password='123')

        self.recipe1 = Recipe.objects.create(name='recipe-1', user=self.user1, batch_size=123)
        self.recipe2 = Recipe.objects.create(name='recipe-2', user=self.user2, batch_size=123)
        self.recipe3 = Recipe.objects.create(name='recipe-3', user=self.user1, batch_size=123)

        for i in range(1, 5):
            Ingredient.objects.create(name='ing' + str(i), amount=i, recipe=self.recipe1)

        for i in range(1, 5):
            Ingredient.objects.create(name='ing' + str(i), amount=i, recipe=self.recipe2)

        for i in range(1, 5):
            Ingredient.objects.create(name='ing' + str(i), amount=i, recipe=self.recipe3)

        self.brew1 = Brew.objects.create(recipe=self.recipe1, note='Note 1', rate=5)
        self.brew2 = Brew.objects.create(recipe=self.recipe1, note='Note 2', rate=3)
        self.brew3 = Brew.objects.create(recipe=self.recipe2, note='Note 3', rate=4)

    def test_rate(self):
        self.client.force_login(self.user1)

        # this is the valid case
        response = self.client.post('/brew/', {f'rate-{self.brew1.pk}': 1})
        self.assertEqual(response.status_code, 200)
        self.brew1.refresh_from_db()
        self.assertEqual(self.brew1.rate, 1)  # should change

        # this rate is out of range, it should be in [1,5]
        response = self.client.post('/brew/', {f'rate-{self.brew2.pk}': 6})
        self.assertEqual(response.status_code, 400)
        self.brew2.refresh_from_db()
        self.assertEqual(self.brew2.rate, 3)  # should not change

        # this brew belongs to different user
        response = self.client.post('/brew/', {f'rate-{self.brew3.pk}': 3})
        self.assertEqual(response.status_code, 401)
        self.brew3.refresh_from_db()
        self.assertEqual(self.brew3.rate, 4)  # should not change

    def test_note(self):
        self.client.force_login(self.user1)
        note = "New Note"

        # this is the valid case
        response = self.client.post('/brew/', {f'comment-{self.brew1.pk}': note})
        self.assertEqual(response.status_code, 200)
        self.brew1.refresh_from_db()
        self.assertEqual(self.brew1.note, note)  # should change

        # this brew belongs to different user
        response = self.client.post('/brew/', {f'comment-{self.brew3.pk}': note})
        self.assertEqual(response.status_code, 401)
        self.brew3.refresh_from_db()
        self.assertNotEqual(self.brew3.note, note)  # should not change
