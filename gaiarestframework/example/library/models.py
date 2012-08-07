from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    class Meta:
        unique_together = (('name', 'surname'),)

    @models.permalink
    def get_absolute_url(self):
        return 'author_info', [self.pk]

class Genre(models.Model):
    description = models.CharField(max_length=50, unique=True)

    @models.permalink
    def get_absolute_url(self):
        return 'genre_info', [self.pk]

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name='books')
    genre = models.ForeignKey(Genre)

    class Meta:
        unique_together = (('title', 'author'),)

    @models.permalink
    def get_absolute_url(self):
        return 'book_info', [self.author.pk, self.pk]

