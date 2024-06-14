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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Avg, Count
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Recipe, MealType, Bookmark, Comment, Rating
from .forms import RecipeForm, CommentForm

# Show 10 recipes per page
MAX_RECORDS = 6


def home_recipe_view(request):
    """
    View for rendering the home page with a list of recipes and a weekly featured recipe.

    This view retrieves the weekly featured recipe and a list of all recipes with their
    average ratings. It paginates the recipe list and renders the home page template with
    the necessary data.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response with the rendered home page template.
    """
    weekly_recipe = Recipe.objects.filter(is_weekly=True).last()
    recipe_list = Recipe.objects.annotate(average_rating=Avg("ratings__rating"))

    # Pagination
    paginator = Paginator(recipe_list, MAX_RECORDS)
    page_number = request.GET.get("page")
    try:
        recipe_list = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recipe_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        recipe_list = paginator.page(paginator.num_pages)

    return render(
        request,
        "home/index.html",
        {
            "weekly_recipe": weekly_recipe,
            "recipe_list": recipe_list,
            "star_range": range(1, 6),
        },
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
        comments = recipe.comments.order_by("-created_on")
        context["comments"] = comments
        context["comment_count"] = comments.filter(approved=True).count()
        context["comment_form"] = CommentForm



        # Retrieve average rating for the recipe
        rating_data = Rating.objects.filter(recipe=recipe).aggregate(
            Avg("rating"), Count("rating")
        )
        context["average_rating"] = rating_data["rating__avg"]
        context["rating_count"] = rating_data["rating__count"]
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
    """
    View for deleting a recipe.

    This view allows authenticated users to delete their own recipes. Only the user who owns
    the recipe can delete it.

    Attributes:
        model (Model): The model class representing the recipe.
        success_url (str): The URL to redirect to after successfully deleting the recipe.

    Methods:
        test_func(): Check if the user is allowed to delete the recipe.
    """

    model = Recipe
    success_url = "/recipes/"

    def test_func(self):
        return self.request.user == self.get_object().user


class EditRecipe(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for editing a recipe.

    This view allows authenticated users to edit their own recipes. Only the user who owns
    the recipe can edit it.

    Attributes:
        template_name (str): The template to render for editing the recipe.
        model (Model): The model class representing the recipe.
        form_class (Form): The form class to use for editing the recipe.
        success_url (str): The URL to redirect to after successfully editing the recipe.

    Methods:
        test_func(): Check if the user is allowed to edit the recipe.
    """

    template_name = "recipes/edit_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = "/recipes/"

    def test_func(self):
        return self.request.user == self.get_object().user


@login_required()
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


@login_required()
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
    """
    View for bookmarking a recipe.

    This view allows authenticated users to bookmark a recipe. If the recipe is not already
    bookmarked by the user, it adds the recipe to the user's bookmarks.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the recipe to be bookmarked.

    Returns:
        HttpResponseRedirect: Redirects to the recipe detail page after bookmarking the recipe.
    """
    if request.method == "GET":
        user = request.user
        recipe = Recipe.objects.get(slug=slug)
        # Check if the recipe is already bookmarked
        if not Bookmark.objects.filter(user=user, recipes=recipe).exists():
            # If not bookmarked, add it to the user's bookmarks
            bookmark, created = Bookmark.objects.get_or_create(user=user)
            bookmark.recipes.add(recipe)
            messages.success(
                request, "Recipe was added to bookmarked list Successfully!"
            )
    # Redirect back to the recipe detail page
    return redirect("recipe_detail", slug=slug)


@login_required
def remove_bookmark(request, slug):
    """
    View for removing a bookmark from a recipe.

    This view allows authenticated users to remove a recipe from their bookmarks.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the recipe to be removed from bookmarks.

    Returns:
        HttpResponseRedirect: Redirects to the recipe detail page after removing the bookmark.
    """
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


@login_required
def rate_recipe(request, recipe_id):
    """
    View for rating a recipe.

    This view allows authenticated users to rate a recipe. It retrieves the rating value
    from the request and updates the rating for the specified recipe.

    Args:
        request (HttpRequest): The HTTP request object.
        recipe_id (int): The ID of the recipe to be rated.

    Returns:
        HttpResponseRedirect: Redirects to the recipe detail page after rating the recipe.
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == "POST":
        rating_value = int(request.POST.get("rating"))
        user = request.user
        try:
            rating = Rating.objects.get(user=user, recipe=recipe)
            rating.rating = rating_value
            rating.save()
        except Rating.DoesNotExist:
            rating = Rating.objects.create(
                user=user, recipe=recipe, rating=rating_value
            )
        # Redirect to the recipe details page after rating submission
        return redirect("recipe_detail", slug=recipe.slug)
    else:
        return redirect("recipe_detail", slug=recipe.slug)


# 404 View
def custom_404(request, exception):
    """
    View for handling 404 errors.

    This view renders a custom 404 page for handling page not found errors.

    Args:
        request (HttpRequest): The HTTP request object.
        exception: The exception object representing the 404 error.

    Returns:
        HttpResponse: The HTTP response with the custom 404 page.
    """
    return render(request, "404.html")
