# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from .models import Recipe, Ingredient, Brew

from django.contrib.auth.mixins import LoginRequiredMixin



class RecipeView(View):
    @staticmethod
    def get(request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)
        brew = recipe.make_brew()

        if brew is None:
            return HttpResponse('You have to buy some ingredients!')

        out = {
            'new brew at': brew.date,
        }

        return HttpResponse(out)


class IngredientView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        ingredients = request.user.ingredient_set.all()
        return render(request, 'index.html', locals())

    @staticmethod
    def post(request):
        ingredients = request.user.ingredient_set.all()
        print(request.POST)
        for ingredient in ingredients:
            if request.POST.get(ingredient.name, None):
                ingredient.amount = float(request.POST[ingredient.name])
                ingredient.save()

        return render(request, "index.html", locals())
