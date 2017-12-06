# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from .models import Recipe, Ingredient, Brew


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

class IngredientView(View):
    @staticmethod
    def get(request):
        return render(request, 'index.html')