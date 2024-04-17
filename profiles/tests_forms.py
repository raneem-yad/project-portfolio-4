from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from .forms import ProfileForm


class ProfileFormTestCase(TestCase):
    def test_profile_form_valid(self):
        with open("./readme/add-recipe.png", "rb") as f:
            image_content = f.read()

        image = SimpleUploadedFile(
            "./readme/add-recipe.png", image_content, content_type="image/jpeg"
        )
        form_data = {
            "image": image,
            "bio": "This is a test bio.",
        }

        form = ProfileForm(data=form_data, files={"image": image})
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_profile_form_invalid(self):
        form_data = {
            # Missing required fields
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors["image"])

