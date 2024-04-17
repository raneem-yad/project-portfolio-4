from django.contrib.auth.models import User
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .forms import RecipeForm, CommentForm
from .models import MealType, Recipe


class RecipeFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='5p.WS%s8X')
        self.client.login(username='test', password='5p.WS%s8X')
        self.meal_type = MealType.objects.create(title='Breakfast')
        self.url = reverse('add_recipe')

    def test_valid_form(self):
        with open("./readme/add-recipe.png", "rb") as f:
            image_content = f.read()

        image = SimpleUploadedFile(
            "./readme/add-recipe.png", image_content, content_type="image/jpeg"
        )

        form_data = {
            "name": "Test Recipe",
            "description": "This is a test recipe description.",
            "instructions": "These are the test recipe instructions.",
            "ingredients": "Ingredient 1\nIngredient 2\nIngredient 3",
            "image": image_content,
            "image_alt": "Test Recipe Image",
            "meal_type": self.meal_type.pk,
            "difficulty": 0,
            "prep_time": 60,
            "serves": 4,
            "status": 0,
        }


        form = RecipeForm(data=form_data, files={"image": image})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Form should be invalid if required fields are missing
        form = RecipeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors["name"])
        self.assertTrue(form.errors["description"])
        self.assertTrue(form.errors["instructions"])
        self.assertTrue(form.errors["ingredients"])
        self.assertTrue(form.errors["image_alt"])
        self.assertTrue(form.errors["meal_type"])
        self.assertTrue(form.errors["difficulty"])
        self.assertTrue(form.errors["prep_time"])
        self.assertTrue(form.errors["serves"])


class CommentFormTestCase(TestCase):
    def test_comment_form_valid(self):
        form_data = {
            "title": "Test Comment",
            "body": "This is a test comment body.",
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        form_data = {
            # Missing required fields
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())