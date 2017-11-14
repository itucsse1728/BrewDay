from django.conf.urls import url, include
from . import views

appname = 'brew'

urlpatterns = [
    url(r'^hello/$', views.HelloWorld.as_view(), name='hello'),
    # url(r'^', include('recipe.urls')),
    # url(r'^', include('ingredient.urls')),
    # url(r'^', include('recommendation.urls')),
]
