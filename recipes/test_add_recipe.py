# from django.test import TestCase
# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth.models import User
# from django.utils.text import slugify
# from .models import Recipe, MealType
# from django.core.files.uploadedfile import SimpleUploadedFile
# from .forms import RecipeForm
# from .views import AddRecipe
#
#
# # Create your tests here.
# class AddRecipeTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='test', password='5p.WS%s8X')
#         self.client.login(username='test', password='5p.WS%s8X')
#         self.meal_type = MealType.objects.create(title='Breakfast')
#         self.url = reverse('add_recipe')
#
#     def test_form_valid(self):
#         meal_type_id = MealType.objects.get(title='Breakfast').id
#         # Create a dummy image file
#         image_content = bytearray([1,2,3])
#         # image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90\x8d6\x00\x00\x00\x0bIDAT\x08\xd7c\x00\x01\x00\x00\x05\x00\x01\r\n\x00\x00\x00\x00IEND\xaeB`\x82'
#         image = SimpleUploadedFile("test_image.png", image_content, content_type="image/png")
#
#         form_data = {
#             'name': 'Test Recipe',
#             'description': 'This is a test recipe description.',
#             'instructions': 'These are the test recipe instructions.',
#             'ingredients': 'Ingredient 1\nIngredient 2\nIngredient 3',
#             'image' :image,
#             'image_alt': 'Test Recipe Image',
#             'meal_type': meal_type_id,
# Provide a valid preparation time in minutes
#             'cooking_time': 60,  # Provide a valid cooking time in minutes
#             'serves': 4,  # P
#         }
#         response = self.client.post(self.url, form_data)
#         # self.assertEqual(response.status_code, 302)  # Check if the form submission redirects
#         print(response.status_code)
#         print(response.body)
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(Recipe.objects.filter(user=self.user, slug=slugify('Test Recipe')).exists())
#
#     def test_form_invalid(self):
#         form_data = {
#             'name': '',  # Empty name field
#         }
#         response = self.client.post(self.url, form_data)
#         self.assertEqual(response.status_code, 200)  # Check if the form submission returns to the same page
#         self.assertFormError(response, 'form', 'name', 'This field is required.')
#         self.assertFormError(response, 'form', 'description',
#                              'This field is required.')
#         self.assertFormError(response, 'form', 'instructions', 'This field is required.')
#         self.assertFormError(response, 'form', 'ingredients', 'This field is required.')
#         self.assertFormError(response, 'form', 'image_alt', 'This field is required.')
#         self.assertFormError(response, 'form', 'meal_type', 'This field is required.')
#
#         self.assertFormError(response, 'form', 'cooking_time', 'This field is required.')
#         self.assertFormError(response, 'form', 'serves', 'This field is required.')
