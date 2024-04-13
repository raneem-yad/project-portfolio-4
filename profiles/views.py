from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProfileForm
from .models import Profile


# Create your views here.
class Profiles(TemplateView):
    template_name = "profiles/profile.html"

    def get_context_data(self, **kwargs):
        profile = Profile.objects.get(user=self.kwargs["pk"])
        context = {
            'profile': profile,
            'profile_form':ProfileForm(instance=profile)
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
