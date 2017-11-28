# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Recipe, Ingredient, Brew
# Register your models here.


@admin.register(Brew)
class BrewAdmin(admin.ModelAdmin):
    list_display = ('date', 'recipe')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'date')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'user', 'recipe')
