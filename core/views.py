# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
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


class BrewView(View):
    @staticmethod
    def get(request):
        brews = Brew.objects.filter(recipe__user=request.user).order_by('-rate', 'date')[:10].\
            select_related('recipe').prefetch_related('recipe__ingredient_set')

        return render(request, 'brew.html', locals())

    @staticmethod
    def post(request):
        for name in request.POST:
            if name.startswith('comment'):
                print(name)
                pk = int(name.split('-')[-1])
                brew = Brew.objects.get(pk=pk)

                if brew.recipe.user != request.user:
                    return HttpResponse('Unauthorized', status=401)

                brew.note = request.POST[name]
                brew.save()
                break

        return redirect('core:brew')


class BrewUpdateRate(View):
    @staticmethod
    def get(request, pk, rate):
        brew = Brew.objects.get(pk=pk)
        rate = int(rate)

        if brew.recipe.user != request.user:
            return HttpResponse('Unauthorized', status=401)

        if rate not in range(1, 6):
            print(rate, '*'*10)
            return HttpResponse('Bad Request', status=400)

        brew.rate = rate
        brew.save()

        return redirect('core:brew')
