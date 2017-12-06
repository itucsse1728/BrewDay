from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('brew/', views.BrewView.as_view(), name='brew'),
    path('brew_update_rate/<int:pk>/<int:rate>/', views.BrewUpdateRate.as_view(), name='brew-update-rate'),
    path('recipe/', views.RecipeView.as_view(), name='recipe'),
    path('brew/', views.BrewView.as_view(), name='brew'),
    path('profile/', views.IngredientView.as_view(), name='profile'),
    path(r'profile/', views.IngredientView.as_view(), name='register'),
    path('recommendation', views.RecommendationView.as_view(), name='recommendation')
]
