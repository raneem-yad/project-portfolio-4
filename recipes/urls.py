from django.urls import path

from .views import AddRecipe, Recipes, RecipeDetail, DeleteRecipe

urlpatterns = [
    path("add_recipe/", AddRecipe.as_view(), name="add_recipe"),
    path("list/", Recipes.as_view(), name="recipes"),
    path('<slug:slug>/', RecipeDetail.as_view(), name='recipe_detail'),
    path('delete/<slug:slug>/', DeleteRecipe.as_view(), name='delete_recipe'),
]
