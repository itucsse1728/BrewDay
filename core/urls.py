from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    url(r'^recipe/(?P<recipe_id>[0-9]+)/$', views.RecipeView.as_view(), name='recipe'),
    url(r'^profile/$', views.IngredientView.as_view(), name='profile'),
    url(r'^profile/$', views.IngredientView.as_view(), name='login'),
    url(r'^profile/$', views.IngredientView.as_view(), name='register'),
]
