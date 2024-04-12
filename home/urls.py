from django.urls import path

from recipes.views import home_recipe_view
urlpatterns = [
    path('', home_recipe_view, name='home'),
]
