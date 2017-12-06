from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Prefetch, Q, F

from .models import Recipe, Ingredient, Brew

from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(View):
    @staticmethod
    def get(request):
        return render(request, 'home.html')

class RecipeView(View):
    @staticmethod
    def get(request):
        recipes = Recipe.objects.filter(user = request.user).order_by('date').prefetch_related('ingredient_set')
        # brew = recipe.make_brew()

        return render(request, 'recipes.html', locals())



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

        if brew.recipe.user != request.user:
            return HttpResponse('Unauthorized', status=401)

        if rate not in range(1, 6):
            print(rate, '*'*10)
            return HttpResponse('Bad Request', status=400)

        brew.rate = rate
        brew.save()

        return redirect('core:brew')
