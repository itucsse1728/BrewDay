from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    batch_size = models.IntegerField()

    def make_brew(self):
        cart = {item.name: item for item in self.user.ingredient_set.all()}
        required = {item.name: item for item in self.ingredient_set.all() if item.amount}

        for name in required:

            if name not in cart or cart[name].amount < required[name].amount:
                return None

            print("1: ", cart[name].amount, " 2: ", required[name].amount)

        for name in required:
            cart[name].amount -= required[name].amount
            cart[name].save()

        user = self.user
        ings = list(self.ingredient_set.all())
        self.pk = None
        self.user = None
        self.save()
        for ingredient in ings:
            print(ingredient)
            ingredient.pk = None
            ingredient.recipe = self
            ingredient.save()

        brew = Brew.objects.create(recipe=self, user=user)
        return brew

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=20)
    amount = models.FloatField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)

    @staticmethod
    def init_ingredients(model, ingredients):
        if isinstance(model, User):
            Ingredient.objects.bulk_create(Ingredient(name=ingredient, amount=0.0, user=model)
                                           for ingredient in ingredients)
        else:
            Ingredient.objects.bulk_create(Ingredient(name=ingredient, amount=0.0, recipe=model)
                                           for ingredient in ingredients)

    def __str__(self):
        return self.name


class Brew(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(max_length=500, null=True, blank=True)
    rate = models.IntegerField(default=3)

    def __str__(self):
        return "{} - {}".format(self.recipe.name, self.date)
