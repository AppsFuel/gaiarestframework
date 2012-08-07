from gaiarestframework.resources import GaiaModelResource
from .models import Author, Book, Genre

class AuthorResource(GaiaModelResource):
    model = Author

class BookResource(GaiaModelResource):
    model = Book

class GenreResource(GaiaModelResource):
    model = Genre