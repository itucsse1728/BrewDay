# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Recipe(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    batch_size = models.IntegerField()

    def make_brew(self):
        cart = {item.name: item for item in self.user.ingredient_set.all()}
        required = {item.name: item for item in self.ingredient_set.all()}

        for name in required:
            if name not in cart or cart[name].amount < required[name].amount:
                return None

        for name in required:
            cart[name].amount -= required[name].amount
            cart[name].save()

        brew = Brew.objects.create(recipe=self)
        return brew

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=20)
    amount = models.FloatField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Brew(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(max_length=500, null=True, blank=True)
    rate = models.IntegerField(default=3)

    def __str__(self):
        return "{} - {}".format(self.recipe.name, self.date)

