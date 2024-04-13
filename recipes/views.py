from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
)
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Recipe, MealType, Bookmark
from .forms import RecipeForm, CommentForm


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
        context["meal_types"] = MealType.objects.all()
        return context

    def get_queryset(self, **kwargs):
        query = self.request.GET.get("q", "")
        meal_type_id = self.request.GET.get("meal_type", "")
        # Start with all recipes
        recipes = self.model.objects.all()

        # Filter by search query if present
        if query:
            recipes = recipes.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(instructions__icontains=query)
            )

        # Filter by meal type if selected
        if meal_type_id:
            recipes = recipes.filter(meal_type_id=meal_type_id)

        return recipes


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Get the current user's bookmarks
            user_bookmarks = Bookmark.objects.filter(user=self.request.user)
            # Check if the current recipe is bookmarked by the user
            context['is_bookmarked'] = user_bookmarks.filter(recipes=self.object).exists()
        else:
            context['is_bookmarked'] = False

        # Comments functionality
        recipe = self.object
        comments = recipe.comments.filter(approved=True).order_by("-created_on")
        comment_count = comments.count()
        if self.request.method == "POST":
            comment_form = CommentForm(data=self.request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = self.request.user
                comment.recipe = recipe
                comment.save()
                # Add success message
                messages.success(
                    self.request,
                    'Comment submitted and awaiting approval'
                )
                # Redirect to the same page after comment submission
                return redirect('recipe_detail', slug=recipe.slug)
        else:
            comment_form = CommentForm()

        # Add comments-related context
        context['comments'] = comments
        context['comment_count'] = comment_count
        context['comment_form'] = comment_form

        return context


class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = "/recipes/"

    def test_func(self):
        return self.request.user == self.get_object().user


class EditRecipe(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "recipes/edit_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = "/recipes/"

    def test_func(self):
        return self.request.user == self.get_object().user


@login_required
def bookmark_recipe(request, slug):
    if request.method == 'GET':
        user = request.user
        recipe = Recipe.objects.get(slug=slug)
        # Check if the recipe is already bookmarked
        if not Bookmark.objects.filter(user=user, recipes=recipe).exists():
            # If not bookmarked, add it to the user's bookmarks
            bookmark, created = Bookmark.objects.get_or_create(user=user)
            bookmark.recipes.add(recipe)
    # Redirect back to the recipe detail page
    return redirect('recipe_detail', slug=slug)


@login_required
def remove_bookmark(request, slug):
    if request.method == 'GET':
        user = request.user
        recipe = Recipe.objects.get(slug=slug)
        # Check if the recipe is bookmarked
        bookmark = Bookmark.objects.filter(user=user, recipes=recipe).first()
        if bookmark:
            # If bookmark exists, remove the recipe from the user's bookmarks
            bookmark.recipes.remove(recipe)
    # Redirect back to the recipe detail page
    return redirect('recipe_detail', slug=slug)
