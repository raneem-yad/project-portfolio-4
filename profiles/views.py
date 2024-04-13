from django.views.generic import  TemplateView
from .models import Profile

# Create your views here.
class Profiles (TemplateView):
    template_name = "profiles/profile.html"

    def get_context_data(self, **kwargs):
        profile = Profile.objects.get(user = self.kwargs["pk"])
        context = {
            'profile' :profile
        }
        return  context