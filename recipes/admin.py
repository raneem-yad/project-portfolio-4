from django.contrib import admin
from .models import Recipe, MealType, Comment, Bookmark


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
