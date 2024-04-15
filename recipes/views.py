from django.shortcuts import render, redirect, get_object_or_404, reverse
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
from django.db.models import Q, Avg, Count
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Recipe, MealType, Bookmark, Comment, Rating
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


class RecipeDetail(FormMixin, DetailView):
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
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object

        # Retrieve bookmarked for the recipe
        if self.request.user.is_authenticated:
            # Get the current user's bookmarks
            user_bookmarks = Bookmark.objects.filter(user=self.request.user)
            # Check if the current recipe is bookmarked by the user
            context["is_bookmarked"] = user_bookmarks.filter(
                recipes=self.object
            ).exists()
        else:
            context["is_bookmarked"] = False

        # Retrieve comments for the recipe
        context["comments"] = recipe.comments.order_by("-created_on")
        context["comment_count"] = context["comments"].count()
        context["comment_form"] = CommentForm

        # Retrieve average rating for the recipe
        rating_data = Rating.objects.filter(recipe=recipe).aggregate(Avg('rating'), Count('rating'))
        context["average_rating"] = rating_data['rating__avg']
        context["rating_count"] = rating_data['rating__count']
        context["star_range"] = range(1, 6)
        return context

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.recipe = recipe
            comment.save()
            # Add success message
            messages.success(self.request, "Comment submitted and awaiting approval")
            # return HttpResponseRedirect(request.path_info)  # Redirect to the same page
            return redirect("recipe_detail", slug=recipe.slug)
        else:
            return self.form_invalid(form)


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


def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":
        recipe = get_object_or_404(Recipe, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        # By specifying instance=comment, any changes made to the form will be applied to the existing Comment,
        # instead of creating a new one.
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, "Comment Updated!")
        else:
            messages.add_message(request, messages.ERROR, "Error updating comment!")

    # reverse is a Django function that constructs a URL from the provided URL path name and any
    # relevant URL arguments: args=[slug].
    return HttpResponseRedirect(reverse("recipe_detail", args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    recipe = get_object_or_404(Recipe, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.ERROR, "Comment deleted!")
    else:
        messages.add_message(
            request, messages.ERROR, "You can only delete your own comments!"
        )

    return HttpResponseRedirect(reverse("recipe_detail", args=[slug]))


@login_required
def bookmark_recipe(request, slug):
    if request.method == "GET":
        user = request.user
        recipe = Recipe.objects.get(slug=slug)
        # Check if the recipe is already bookmarked
        if not Bookmark.objects.filter(user=user, recipes=recipe).exists():
            # If not bookmarked, add it to the user's bookmarks
            bookmark, created = Bookmark.objects.get_or_create(user=user)
            bookmark.recipes.add(recipe)
            messages.success(request, "Recipe was booked Successfully!")
    # Redirect back to the recipe detail page
    return redirect("recipe_detail", slug=slug)


@login_required
def remove_bookmark(request, slug):
    if request.method == "GET":
        user = request.user
        recipe = Recipe.objects.get(slug=slug)
        # Check if the recipe is bookmarked
        bookmark = Bookmark.objects.filter(user=user, recipes=recipe).first()
        if bookmark:
            # If bookmark exists, remove the recipe from the user's bookmarks
            bookmark.recipes.remove(recipe)
            messages.success(
                request, "Recipe was removed from bookmarked list Successfully!"
            )
    # Redirect back to the recipe detail page
    return redirect("recipe_detail", slug=slug)


def rate_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.recipe = recipe
            rating.save()
            return redirect('recipe_detail', slug=recipe.slug)
    else:
        form = RatingForm()
    return render(request, 'recipe_details.html', {'rating_form': form, 'recipe': recipe})