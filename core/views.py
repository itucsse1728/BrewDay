# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from .models import Recipe, Ingredient, Brew


class RecipeView(View):
    @staticmethod
    def get(request):
        recipes = Recipe.objects.filter(user = request.user).order_by('date').prefetch_related('ingredient_set')
        # brew = recipe.make_brew()

        return render(request, 'recipes.html', locals())

class IngredientView(View):
    @staticmethod
    def get(request):
        return render(request, 'index.html')