from django import forms
from djrichtextfield.widgets import RichTextWidget
from .models import Recipe, Comment


class RecipeForm(forms.ModelForm):
    """Form to create a recipe"""

    class Meta:
        model = Recipe
        fields = [
            "name",
            "description",
            "instructions",
            "ingredients",
            "image",
            "image_alt",
            "meal_type",
            "difficulty",
            "prep_time",
            "serves",
        ]
        ingredients = forms.CharField(widget=RichTextWidget())
        instructions = forms.CharField(widget=RichTextWidget())
        widget = {"description": forms.Textarea(attrs={"row": 5})}
        labels = {
            "name": "Recipe Name",
            "description": "Some More Description about the Recipe",
            "instructions": "The recipe instructions ",
            "ingredients": "The Recipe Ingredients",
            "image": "Image of your Recipe",
            "image_alt": "Description of your Image",
            "meal_type": "Pick which meal type your recipe is!",
            "difficulty": "Difficulty",
            "prep_time": "Cooking time in minutes",
            "serves": "Serves",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "title",
            "body",
        ]
        widget = {"body": forms.Textarea(attrs={"row": 5})}
        labels = {
            "title": "Comment Title",
            "body": "Tell us how you found the Recipe",
        }
