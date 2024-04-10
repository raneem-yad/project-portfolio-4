from django.contrib import admin
from .models import Recipe,MealType,Comment

# Register your models here.
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'meal_type',
        'instructions',
        'ingredients',
        'image'
    )
    list_filter = (('meal_type',))


@admin.register(MealType)
class MealTypeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'approved'
    )