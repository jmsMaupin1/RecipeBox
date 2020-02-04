from django.shortcuts import render, reverse, HttpResponseRedirect
from recipe.models import Recipes, Author
from recipe.forms import addRecipe, addAuthor


def index(request):
    item = Recipes.objects.all()
    return render(request, 'recipes/index.html', {'data': item})


def detail(request, id):
    item = Recipes.objects.get(id=id)
    return render(request, 'recipes/detail.html', {'data': item})


def author(request, id):
    item = Author.objects.get(id=id)
    recipe = Recipes.objects.filter(author=item)
    return render(
        request, 'recipes/author.html', {'data': item, 'recipe': recipe})


def recipe_add(request):
    html = 'addRecipe.html'

    if request.method == 'POST':
        form = addRecipe(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            Recipes.objects.create(
                title=data['title'],
                description=data['description'],
                author=data['author'],
                instructions=data['instructions']
            )
            return HttpResponseRedirect(reverse("main"))

    form = addRecipe()

    return render(request, html, {'form': form})


def author_add(request):
    html = 'addAuthor.html'

    if request.method == 'POST':
        form = addAuthor(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            Author.objects.create(
                name=data['name'],
                bio=data['bio']
            )
            return HttpResponseRedirect(reverse("main"))

    form = addAuthor()

    return render(request, html, {'form': form})
