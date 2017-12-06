from django.test import TestCase

from .models import Recipe, Ingredient, User


class TestVerification(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='dummy@dmail.com',
                                             email='dummy@dmail.com',
                                             password='123')
        self.recipe = Recipe.objects.create(name='recipe1',
                                            user=self.user,
                                            batch_size=123)

        for i in range(1, 11):
            Ingredient.objects.create(name='ing'+ str(i),
                                      amount=i,
                                      user=self.user)

        for i in range(1, 11):
            Ingredient.objects.create(name='ing'+ str(i),
                                      amount=2*i-5,
                                      recipe=self.recipe)

        self.recipe2 = Recipe.objects.create(name='recipe2',
                                             user=self.user,
                                             batch_size=123)

        for i in range(1, 5):
            Ingredient.objects.create(name='ing' + str(i),
                                      amount=i,
                                      recipe=self.recipe2)


    def test_recomm(self):
        self.client.force_login(self.user)
        response = self.client.post('/recommendation')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['recipes']),2)