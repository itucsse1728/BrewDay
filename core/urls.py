from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(success_url='/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('recipe/', views.RecipeView.as_view(), name='recipe'),
    path('brew/', views.BrewView.as_view(), name='brew'),
    path('profile/', views.IngredientView.as_view(), name='profile'),
    path(r'profile/', views.IngredientView.as_view(), name='register'),
    path('recommendation', views.RecommendationView.as_view(), name='recommendation')
]
