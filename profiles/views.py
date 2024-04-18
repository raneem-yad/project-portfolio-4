from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProfileForm
from .models import Profile


# Create your views here.
class Profiles(TemplateView):
    """
    View for displaying user profiles.

    This view retrieves the user profile information based on the provided user ID (pk)
    and renders the profile template with the profile data and a list of bookmarked recipes.

    Attributes:
        template_name (str): The template to render the user profile.

    Methods:
        get_context_data(**kwargs): Retrieve the user profile and associated bookmarked recipes
            to pass to the template context.
    """

    template_name = "profiles/profile.html"

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        profile = Profile.objects.get(user=self.kwargs["pk"])
        bookmarked_recipes = user.bookmarks.values_list(
            "recipes__name", "recipes__slug"
        )

        context = {
            "profile": profile,
            "bookmarked_recipes": bookmarked_recipes,
            "profile_form": ProfileForm(instance=profile),
        }
        return context


class EditProfile(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for editing user profiles.

    This view allows authenticated users to edit their own profiles. Only the user who owns
    the profile can edit it.

    Attributes:
        form_class (Form): The form class to use for editing the profile.
        model (Model): The model class representing the profile.
    """

    form_class = ProfileForm
    model = Profile

    def form_valid(self, form):
        self.success_url = f'/profiles/user/{self.kwargs["pk"]}/'
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().user
