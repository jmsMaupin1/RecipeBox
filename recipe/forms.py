from django import forms
from crispy_forms.helper import FormHelper
from recipe.models import Author, Recipes
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class addRecipe(forms.Form):
    helper = FormHelper()
    helper.form_show_labels = True
    title = forms.CharField(max_length=30)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    instructions = forms.CharField(widget=forms.Textarea)


class addAuthor(forms.Form):
    name = forms.CharField(max_length=20)
    bio = forms.CharField(widget=forms.Textarea)


class CreateUserForm(UserCreationForm):
    class meta:
        model = User
        fields = ['username', 'passowrd1', 'password2']


class EditRecipe(forms.ModelForm):
    class Meta:
        model = Recipes
        fields = [
            'title',
            'description',
            'timeRequired',
            'instructions',
            'ingredients'
        ]