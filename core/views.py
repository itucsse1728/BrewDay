from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Prefetch, Q
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Recipe, Ingredient, Brew
from .forms import RegisterForm

INGREDIENTS = (
    'malt',
    'hops',
    'yeast',
    'sugar',
    'additive'
)


class HomeView(View):
    @staticmethod
    def get(request):
        return render(request, 'home.html')
      

class RecipeView(View):
    @staticmethod
    def get(request):
        recipes = Recipe.objects.filter(user=request.user).order_by('date').prefetch_related('ingredient_set')
        # brew = recipe.make_brew()
        return render(request, 'recipes.html', locals())

    @staticmethod
    def post(request):
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

        return render(request, 'recipes.html', locals())


class IngredientView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        ingredients = request.user.ingredient_set.all()
        return render(request, 'index.html', locals())

    @staticmethod
    def post(request):
        ingredients = request.user.ingredient_set.all()
        for ingredient in ingredients:
            if request.POST.get(ingredient.name, None):
                ingredient.amount = float(request.POST[ingredient.name])
                ingredient.save()

            #if request.POST.get("new-ingredient-name", None) and request.POST.get("new-ingredient-amount", None):



        return render(request, "index.html", locals())


class RecommendationView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        ingredients = request.user.ingredient_set.all()
        return render(request, 'recommendation.html', locals())

    @staticmethod
    def post(request):
        ingredients = request.user.ingredient_set.all()
        ings = {ing.name: ing.amount for ing in ingredients}
        queryset = Ingredient.objects.filter(name__in=ings)

        recipes = Recipe.objects.prefetch_related(
            Prefetch('ingredient_set',
                     queryset=queryset)
            ).exclude(~Q(ingredient__name__in=ings))

        for name, amount in ings.items():
            recipes.filter(~Q(ingredient__name=name) | Q(ingredient__amount__lt=amount))

        return render(request, 'recommendation.html', locals())


class BrewView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        brews = Brew.objects.filter(recipe__user=request.user).order_by('-rate', 'date')[:10].\
            select_related('recipe').prefetch_related('recipe__ingredient_set')

        return render(request, 'brew.html', {'brews': brews})

    @staticmethod
    def post(request):
        for name in request.POST:
            if name.startswith('comment'):
                pk = int(name.split('-')[-1])
                brew = Brew.objects.get(pk=pk)

                if brew.recipe.user != request.user:
                    return HttpResponse('Unauthorized', status=401)

                brew.note = request.POST[name]
                brew.save()
                break

            if name.startswith('rate'):
                pk = int(name.split('-')[-1])
                brew = Brew.objects.get(pk=pk)
                rate = int(request.POST[name])

                if brew.recipe.user != request.user:
                    return HttpResponse('Unauthorized', status=401)

                if rate not in range(1, 6):
                    return HttpResponse('Bad Request', status=400)

                brew.rate = rate
                brew.save()
                break

        brews = Brew.objects.filter(recipe__user=request.user).order_by('-rate', 'date')[:10]. \
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
        Ingredient.init_ingredients(self.object, INGREDIENTS)
        self.object.save()
        login(self.request, self.object)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
