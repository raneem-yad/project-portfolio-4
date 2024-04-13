from django.urls import path

from .views import AddRecipe, Recipes, RecipeDetail, DeleteRecipe, EditRecipe, bookmark_recipe, remove_bookmark

urlpatterns = [
    path("add_recipe/", AddRecipe.as_view(), name="add_recipe"),
    path("<slug:slug>/", RecipeDetail.as_view(), name="recipe_detail"),
    path("delete/<slug:slug>/", DeleteRecipe.as_view(), name="delete_recipe"),
    path("edit/<slug:slug>/", EditRecipe.as_view(), name="edit_recipe"),
    path('bookmark/<slug:slug>/', bookmark_recipe, name='bookmark_recipe'),
    path('remove-bookmark/<slug:slug>/', remove_bookmark, name='remove_bookmark'),
    path("", Recipes.as_view(), name="recipes"),
]
