from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    url(r'^recipe/$', views.RecipeView.as_view(), name='recipe'),
    url(r'^brew/$', views.BrewView.as_view(), name='brew'),
    url(r'^profile/$', views.IngredientView.as_view(), name='profile'),
    url(r'^profile/$', views.IngredientView.as_view(), name='login'),
    url(r'^logout/$', views.IngredientView.as_view(), name='logout'),
    url(r'^profile/$', views.IngredientView.as_view(), name='register'),
]
