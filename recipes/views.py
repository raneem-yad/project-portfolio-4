from django.views.generic import CreateView
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe
from .forms import RecipeForm


# Create your views here.
class AddRecipe(LoginRequiredMixin, CreateView):
    """
    Add recipe View
    """
    template_name = 'recipes/add_recipe.html'
    model = Recipe
    form_class = RecipeForm
    success_url = '/recipes/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        recipe_name = form.cleaned_data.get('name')
        form.instance.slug = slugify(recipe_name)
        form.instance.is_weekly = False
        return super(AddRecipe, self).form_valid(form)
