from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch, Q, F, Count
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Recipe, Ingredient, Brew
from .forms import RegisterForm

INGREDIENTS = (
    'Malt',
    'Hops',
    'Yeast',
    'Sugar',
    'Additive'
)


class HomeView(View):
    @staticmethod
    def get(request):
        return render(request, 'home.html')
      

class RecipeView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        recipes = Recipe.objects.filter(user=request.user).order_by('date').prefetch_related('ingredient_set')
        # brew = recipe.make_brew()
        return render(request, 'recipes.html', locals())

    @staticmethod
    def post(request):
        ingredient_name = request.POST.get("new-ingredient-name", None)
        ingredient_amount = request.POST.get("new-ingredient-amount", None)
        flag = False

        recipes = Recipe.objects.filter(user=request.user).order_by('date').prefetch_related('ingredient_set')
        recipeName = ""
        if request.POST.get('recipeName', None):
            recipeName = str(request.POST['recipeName'])
        recipe = Recipe.objects.create(name=recipeName, batch_size=11, user = request.user)
        for ingredient in INGREDIENTS:
            if request.POST.get(ingredient, None):
                amount = float(request.POST[ingredient])
            else:
                amount = float(0)
            ingre = Ingredient.objects.create(name = ingredient, amount = amount, recipe = recipe)

            if ingredient == ingredient_name:
                flag = True

        if ingredient_name and ingredient_amount and not flag:
            ingredient = Ingredient(name=ingredient_name, amount=ingredient_amount, recipe=recipe)
            ingredient.save()

        return render(request, 'recipes.html', locals())


class RecipeManagement(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        flag = False
        recipe_id = request.POST.get("recipe-id", None)

        recipe = get_object_or_404(Recipe, pk=recipe_id)

        if "brew" in request.POST:
            recipe.make_brew()

        elif "update" in request.POST:
            ingredients = list(recipe.ingredient_set.all())

            ingredient_name = request.POST.get("new-ingredient-name", None)
            ingredient_amount = request.POST.get("new-ingredient-amount", None)

            for ingredient in ingredients:
                if request.POST.get(ingredient.name, None):
                    ingredient.amount = float(request.POST[ingredient.name])
                    ingredient.save()

                if ingredient.name == ingredient_name:
                    flag = True

            if ingredient_name and ingredient_amount and not flag:
                ingredient = Ingredient(name=ingredient_name, amount=float(ingredient_amount), recipe=recipe)
                ingredient.save()

        else:
            recipe.delete()

        return redirect("core:recipe")




class IngredientView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        ingredients = request.user.ingredient_set.all()
        return render(request, 'index.html', locals())

    @staticmethod
    def post(request):
        flag = False

        ingredients = request.user.ingredient_set.all()

        if "delete" in request.POST:
            ingredient_id = request.POST.get("delete")

            get_object_or_404(Ingredient.objects.select_related("user"), pk=ingredient_id, user=request.user).delete()

        else:
            ingredients = list(ingredients)
            ingredient_name = request.POST.get("new-ingredient-name", None)
            ingredient_amount = request.POST.get("new-ingredient-amount", None)

            for ingredient in ingredients:
                if request.POST.get(ingredient.name, None):
                    ingredient.amount = float(request.POST[ingredient.name])
                    ingredient.save()

                if ingredient.name == ingredient_name:
                    flag = True

            if ingredient_name and ingredient_amount and not flag:
                ingredient = Ingredient(name=ingredient_name, amount=float(ingredient_amount), user=request.user)
                ingredient.save()
                ingredients.append(ingredient)


        return render(request, "index.html", locals())


class RecommendationView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        ingredients = request.user.ingredient_set.all()
        return render(request, 'recommendation.html', locals())

    @staticmethod
    def post(request):
        ingredients = request.user.ingredient_set.all()
        self_ings = {ing.name: ing.amount for ing in ingredients if ing.amount}

        recipes = Recipe.objects.prefetch_related('ingredient_set')

        recipes = {i:recipe for i, recipe in enumerate(recipes)}
        output = []

        for i, recipe in recipes.items():
            for ingredient in recipe.ingredient_set.all():
                if ingredient.name not in self_ings and ingredient.amount > 0.0:
                    break
                elif ingredient.name in self_ings and ingredient.amount > self_ings[ingredient.name]:
                    break
            else:
                output.append(i)

        recipes = [recipes[i] for i in output]

        return render(request, 'recommendation.html', locals())

class BrewView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        brews = Brew.objects.filter(user=request.user).order_by('-rate', 'date')[:10].\
            select_related('recipe').prefetch_related('recipe__ingredient_set')

        return render(request, 'brew.html', {'brews': brews})

    @staticmethod
    def post(request):
        for name in request.POST:
            if name.startswith('comment'):
                pk = int(name.split('-')[-1])
                brew = Brew.objects.get(pk=pk)

                if brew.user != request.user:
                    return HttpResponse('Unauthorized', status=401)

                brew.note = request.POST[name]
                brew.save()
                break

            if name.startswith('rate'):
                pk = int(name.split('-')[-1])
                brew = Brew.objects.get(pk=pk)
                rate = int(request.POST[name])

                if brew.user != request.user:
                    return HttpResponse('Unauthorized', status=401)

                if rate not in range(1, 6):
                    return HttpResponse('Bad Request', status=400)

                brew.rate = rate
                brew.save()
                break

        brews = Brew.objects.filter(user=request.user).order_by('-rate', 'date')[:10]. \
            select_related('recipe').prefetch_related('recipe__ingredient_set')

        return render(request, 'brew.html', {'brews': brews})


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        if self.request.POST.get('password2') != form.cleaned_data.get('password'):
            return self.form_invalid(form)

        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data.get('password'))
        self.object.save()
        Ingredient.init_ingredients(self.object, INGREDIENTS)
        login(self.request, self.object)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
