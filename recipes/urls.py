from django.urls import path

from .views import AddRecipe, Recipes

urlpatterns = [
    path("add_recipe/", AddRecipe.as_view(), name="add_recipe"),
    path("list/", Recipes.as_view(), name="recipes"),
]
