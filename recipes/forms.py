from django import forms
from djrichtextfield.widgets import RichTextWidget
from .models import Recipe


class RecipeForm(forms.ModelForm):
    """Form to create a recipe """

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions', 'ingredients', 'image', 'image_alt', 'meal_type', 'difficulty',
                  'preparation_time', 'cooking_time', 'serves', 'status']
        ingredients = forms.CharField(widget=RichTextWidget())
        instructions = forms.CharField(widget=RichTextWidget())
        widget = {
            'description': forms.Textarea(attrs={'row': 5})
        }
        labels = {
            'name': 'Recipe Name',
            'description': 'Some More Description about the Recipe',
            'instructions': 'How we can make your Recipe (instructions) ',
            'ingredients': 'What are the Recipe Ingredients',
            'image': 'Image of your Recipe',
            'image_alt': 'Description of your Image',
            'meal_type': 'Pick which meal type your recipe is!',
            'difficulty': 'Difficulty',
            'preparation_time': 'Preparation Time',
            'cooking_time': 'Cooking time',
            'serves': 'Serves'
        }
