from django import forms
from recipe.models import Author


class addRecipe(forms.Form):
    title = forms.CharField(max_length=30)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    instructions = forms.CharField(widget=forms.Textarea)


class addAuthor(forms.Form):
    name = forms.CharField(max_length=20)
    bio = forms.CharField(widget=forms.Textarea)
