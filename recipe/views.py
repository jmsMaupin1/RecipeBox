# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, reverse, HttpResponseRedirect, redirect
from recipe.models import Recipes, Author
from recipe.forms import addRecipe, addAuthor, EditRecipe
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from .decorators import unauth_user, allowed_users
from django.contrib.auth.decorators import permission_required

@unauth_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            Author.objects.create(
                name=user,
                bio=''
            )
            messages.success(request, "Account created for " + user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'recipes/register.html', context)


@unauth_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("main")
        else:
            messages.info(request, 'Username or password is incorrect.')
    return render(request, 'recipes/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    item = Recipes.objects.all()
    return render(request, 'recipes/index.html', {'data': item})


@login_required(login_url='login')
def detail(request, id):
    item = Recipes.objects.get(id=id)
    is_superuser = request.user.is_superuser
    logged_in_author = Author.objects.get(name=request.user.username)
    allow_edit = is_superuser or logged_in_author.name == item.author.name
    return render(request, 'recipes/detail.html', {
            'data': item,
            'allow_edit': allow_edit
        }
    )


@login_required(login_url='login')
def author(request, id):
    item = Author.objects.get(id=id)
    recipe = Recipes.objects.filter(author=item)
    favorites = item.favorites.all()
    return render(
        request, 'recipes/author.html', {
            'data': item,
            'recipe': recipe,
            'favorites': favorites
        }
    )


@login_required(login_url='login')
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'author'])
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


def add_favorite(request, recipe_id):
    recipe = None
    user = None
    
    try:
        recipe = Recipes.objects.get(id=recipe_id)
        user = Author.objects.get(name=request.user.username)
        user.favorites.add(recipe)
        user.save()
    except Exception as e:
        print(e)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def edit_recipe_view(request, recipe_id):
    recipe = None
    form = None

    try:
        recipe = Recipes.objects.get(id=recipe_id)
    except Exception as e:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == 'POST':
        form = EditRecipe(request.POST, instance=recipe)

        if form.is_valid():
            form.save()
        
        return HttpResponseRedirect(reverse('main'))
    
    else:
        form = EditRecipe(instance=recipe)

    return render(request, 'generic_form.html', {'form': form})


# def register(response):
#     if response.method == "POST":
#         form = UserCreationForm(response.POST)
#         if form.is_valid():
#             form.save()

#     form = UserCreationForm()
#     return render(response, "register/register.html", {"form": form})


def dnuse(request):
    context = {}
    template = "dnu.html"
    return render(request, template, context)



