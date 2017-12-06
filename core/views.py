from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Prefetch, Q, F

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


class RecommendationView(View):
    @staticmethod
    def get(request):
        ingredients = request.user.ingredient_set.all()
        return render(request, 'recommendation.html', locals())

    @staticmethod
    def post(request):
        ingredients = request.user.ingredient_set.all()
        ings = {ing.name:ing.amount for ing in ingredients}
        queryset = Ingredient.objects.filter(name__in=ings)

        recipes = Recipe.objects.prefetch_related(
            Prefetch('ingredient_set',
                     queryset=queryset)
            ).exclude(~Q(ingredient__name__in=ings))


        for name, amount in ings.items():
            recipes.filter( ~Q(ingredient__name=name) | Q(ingredient__amount__lt=amount) )

        return render(request, 'recommendation.html', locals())


class BrewView(View):
    @staticmethod
    def get(request):
        brews = Brew.objects.filter(recipe__user=request.user).order_by('date')[:10].\
            select_related('recipe').prefetch_related('recipe__ingredient_set')
        return render(request, 'brew.html', locals())
