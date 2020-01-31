from django.db import models


class Recipes(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    description = models.TextField()
    timeRequired = models.CharField("Cooking Time", max_length=100)
    instructions = models.TextField()
    ingredients = models.TextField()

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField("Author", max_length=20)
    bio = models.TextField()

    def __str__(self):
        # return "{} - {}".format(self.name, self.bio)
        return self.name
