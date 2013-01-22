from django import forms
from gaiarestframework.resources import GaiaModelResource
from .models import Author, Book, Genre

class AuthorResource(GaiaModelResource):
    model = Author

class BookResource(GaiaModelResource):
    model = Book

class GenreForm(forms.ModelForm):
    toremove = forms.BooleanField()
    class Meta:
        model = Genre

class GenreResource(GaiaModelResource):
    model = Genre
    form = GenreForm
