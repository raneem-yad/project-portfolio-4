from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.utils.text import slugify
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.db.models import Q
from .models import Recipe, MealType
from .forms import RecipeForm


# Create your views here.
def home_recipe_view(request):
    weekly_recipe = Recipe.objects.filter(is_weekly=True).last()
    recipe_list = Recipe.objects.all()
    return render(
        request,
        "home/index.html",
        {"weekly_recipe": weekly_recipe, "recipe_list": recipe_list},
    )


class Recipes(ListView):
    """
    List recipe View
    """

    template_name = "recipes/recipes.html"
    model = Recipe
    context_object_name = "recipes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meal_types'] = MealType.objects.all()
        return context

    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q','')
        meal_type_id = self.request.GET.get('meal_type', '')
        # Start with all recipes
        recipes = self.model.objects.all()

        # Filter by search query if present
        if query:
            recipes = recipes.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(instructions__icontains=query)
            )

        # Filter by meal type if selected
        if meal_type_id:
            recipes = recipes.filter(meal_type_id=meal_type_id)

        return recipes
        # if query:
        #     recipes = self.model.objects.filter(
        #         Q(name__icontains=query) |
        #         Q(description__icontains=query) |
        #         Q(instructions__icontains=query)
        #     )
        # else:
        #     recipes = self.model.objects.all()
        # return recipes


class AddRecipe(LoginRequiredMixin, CreateView):
    """
    Add recipe View
    """

    template_name = "recipes/add_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = "/recipes/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        recipe_name = form.cleaned_data.get("name")
        form.instance.slug = slugify(recipe_name)
        form.instance.is_weekly = False
        return super(AddRecipe, self).form_valid(form)


class RecipeDetail(DetailView):
    """
    Display an individual :model:`Recipe`.

    **Context**

    ``Recipe``
        An instance of :model:`Recipe`.

    **Template:**

    :template:`blog/Recipe_detail.html`
    """

    template_name = "recipes/recipe_details.html"
    model = Recipe
    context_object_name = "recipe"


class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = '/recipes/'

    def test_func(self):
        return self.request.user == self.get_object().user


class EditRecipe(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "recipes/edit_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = '/recipes/'

    def test_func(self):
        return self.request.user == self.get_object().user
