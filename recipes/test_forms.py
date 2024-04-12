from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import RecipeForm
from .models import MealType, Recipe


class RecipeFormTestCase(TestCase):
    def setUp(self):
        # Create a MealType instance for testing
        self.meal_type = MealType.objects.create(title="Breakfast")

    def test_valid_form(self):
        # Create a dummy image file
        image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90\x8d6\x00\x00\x00\x0bIDAT\x08\xd7c\x00\x01\x00\x00\x05\x00\x01\r\n\x00\x00\x00\x00IEND\xaeB`\x82"
        image = SimpleUploadedFile(
            "test_image.png", image_content, content_type="image/png"
        )

        form_data = {
            "name": "Test Recipe",
            "description": "This is a test recipe description.",
            "instructions": "These are the test recipe instructions.",
            "ingredients": "Ingredient 1\nIngredient 2\nIngredient 3",
            "image": image,
            "image_alt": "Test Recipe Image",
            "meal_type": self.meal_type.pk,
            "difficulty": 0,
            "preparation_time": 30,
            "cooking_time": 60,
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
        self.assertTrue(form.errors["preparation_time"])
        self.assertTrue(form.errors["cooking_time"])
        self.assertTrue(form.errors["serves"])
