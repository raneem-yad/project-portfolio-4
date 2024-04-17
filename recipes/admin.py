from django.contrib import admin
from django.db.models import Avg

from .models import Recipe, MealType, Comment, Bookmark, Rating


# Register your models here.
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "meal_type", "instructions", "ingredients", "image")
    list_filter = ("meal_type",)


@admin.register(MealType)
class MealTypeAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "approved")


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "display_recipes")

    def display_recipes(self, obj):
        return ", ".join([recipe.name for recipe in obj.recipes.all()])


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "display_recipe", "rating", "average_rate")

    def display_recipe(self, obj):
        return obj.recipe.name

    def average_rate(self, obj):
        average_rating = Rating.objects.filter(recipe=obj.recipe).aggregate(
            Avg("rating")
        )["rating__avg"]
        return average_rating if average_rating is not None else 0
