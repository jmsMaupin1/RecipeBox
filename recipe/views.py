from django.shortcuts import render
from recipe.models import Recipes, Author


def index(request):
    item = Recipes.objects.all()
    # items2 = Author.objects.all()
    return render(request, 'recipes/index.html', {'data': item})


def detail(request, id):
    item = Recipes.objects.get(id=id)
    return render(request, 'recipes/detail.html', {'data': item})


def author(request, id):
    item = Author.objects.get(id=id)
    recipe = Recipes.objects.filter(author=item)
    return render(
        request, 'recipes/author.html', {'data': item, 'recipe': recipe})
