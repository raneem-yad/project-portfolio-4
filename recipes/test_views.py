from django.test import TestCase, RequestFactory
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Avg
from .views import home_recipe_view
from .models import Recipe


class HomeRecipeViewTestCase(TestCase):
    def setUp(self):
        # Create sample data
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            is_weekly=True,
        )
        # Create some ratings for the recipe
        self.recipe.ratings.create(rating=4, user=self.user)
        self.recipe.ratings.create(rating=5, user=self.user)

    def test_home_recipe_view(self):
        # Create a GET request
        request = self.factory.get("/")
        response = home_recipe_view(request)

        # Check if the view returns a successful response
        self.assertEqual(response.status_code, 200)

        # Check if the correct context variables are passed to the template
        self.assertIn("weekly_recipe", response.context)
        self.assertIn("recipe_list", response.context)
        self.assertIn("star_range", response.context)

        # Check if pagination is working correctly
        paginator = Paginator(response.context["recipe_list"], 10)  # Assuming 10 items per page
        self.assertTrue(paginator.num_pages >= 1)  # At least one page should exist
