from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from djrichtextfield.models import RichTextField
from django_resized import ResizedImageField

# Choices here
DIFFICULTY = ((0, "Easy"), (1, "Medium"), (2, "Hard"))


# Create your models here.
class MealType(models.Model):
    """
    A model to represent meal types.
    """

    title = models.CharField(max_length=50)

    def __str__(self):
        return str(self.title)


class Recipe(models.Model):
    """
    Model to create recipe
    """

    user = models.ForeignKey(
        User, related_name="recipe_owner", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=300, unique=True, null=False, blank=False)
    slug = models.SlugField(max_length=300, unique=True)
    description = models.CharField(max_length=500, null=False, blank=False)
    instructions = RichTextField(max_length=10000, null=False, blank=False)
    ingredients = RichTextField(max_length=10000, null=False, blank=False)
    image = ResizedImageField(
        size=[400, None],
        quality=85,
        upload_to="recipes/",
        # force_format="WEBP,PNG,JPNG",
        null=False,
        blank=False,
    )
    image_alt = models.CharField(max_length=100, null=False, blank=False)
    meal_type = models.ForeignKey(
        MealType, related_name="recipe_type", on_delete=models.CASCADE
    )
    is_weekly = models.BooleanField(default=False)
    difficulty = models.IntegerField(choices=DIFFICULTY, default=0)
    serves = models.PositiveIntegerField()
    prep_time = models.PositiveIntegerField(default=1)
    posted_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-posted_date"]

    def __str__(self):
        return str(self.name)


class Comment(models.Model):
    title = models.CharField(max_length=200, default="Wonderful Recipe")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment {self.title} by {self.author}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, related_name="bookmarks", on_delete=models.CASCADE)
    recipes = models.ManyToManyField("recipes.Recipe")


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rater")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f"{self.recipe} - {self.user}: {self.rating} stars"

    class Meta:
        unique_together = ("recipe", "user")  # Each user can rate a recipe only once

    @classmethod
    def get_average_rating(cls, recipe_id):
        average_rating = cls.objects.filter(recipe_id=recipe_id).aggregate(
            Avg("rating")
        )["rating__avg"]
        return average_rating or 0
