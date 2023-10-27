from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import validators
from django.core.validators import MinValueValidator
from django.db import models

category_choices = [
    ("Home", "Home"),
    ("Fashion", "Fashion"),
    ("Toys", "Toys"),
    ("Electronics", "Electronics"),
]


class ListingModel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=300)
    i_bid = models.PositiveIntegerField()
    owner = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    category = models.CharField(
        max_length=20,
    )

    def __str__(self):
        return f"{self.title} at in {self.category}"


class User(AbstractUser):
    watchlist = models.ManyToManyField(
        ListingModel,
        blank=True,
        related_name="interested_users",
    )
