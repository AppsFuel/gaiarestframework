from gaiarestframework import testutils
from django.core.urlresolvers import reverse
from example.library.models import Book, Author


class BookListTestCase(testutils.GaiaTestCase):
    fixtures = ['user.json', 'author.json', 'book.json', 'genre.json']
    resource_cls = Book
    resource_list_path = reverse('book_list', kwargs={'author': 1})
    resource_instance_path = reverse('book_info', kwargs={'author': 1, 'id': 1})
    resource = {
        'title': 'Gregor the Overlander',
        'author': 1,
        'genre': "Fantasy",
    }

    def get_object_dict(self, item):
        return dict(
            title=item['title'],
            author__name=item['author']['name'],
            author__surname=item['author']['surname'],
        )

    def get_assertion_dict(self, object):
        return {
            'url': reverse('book_info',
                kwargs={'author': object.author.id, 'id': object.id},
                prefix='http://testserver/'),
        }
