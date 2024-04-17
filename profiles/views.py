from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProfileForm
from .models import Profile


# Create your views here.
class Profiles(TemplateView):
    template_name = "profiles/profile.html"

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        profile = Profile.objects.get(user=self.kwargs["pk"])
        print(user)
        print("==================")
        print(user.bookmarks)
        print("==================")
        print(user.bookmarks.values_list("recipes__name", flat=True))
        print("==================")
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
    form_class = ProfileForm
    model = Profile

    def form_valid(self, form):
        self.success_url = f'/profiles/user/{self.kwargs["pk"]}/'
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().user
