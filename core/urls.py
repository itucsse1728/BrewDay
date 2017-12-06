from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(success_url='/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^recipe/(?P<recipe_id>[0-9]+)/$', views.RecipeView.as_view(), name='recipe'),
    url(r'^profile/$', views.IngredientView.as_view(), name='profile'),
    url(r'^profile/$', views.IngredientView.as_view(), name='register'),
    path('recommendation', views.RecommendationView.as_view(), name='recommendation'),

]
