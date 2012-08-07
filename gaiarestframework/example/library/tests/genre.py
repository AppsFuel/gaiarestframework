from gaiarestframework import testutils
from django.core.urlresolvers import reverse
from example.library.models import Genre


class GenreListTestCase(testutils.GaiaTestCase):
    fixtures = ['user.json', 'genre.json', ]
    resource_cls = Genre
    resource = {'description': 'Thriller', }
    resource_list_path = reverse('genre_list')
    resource_instance_path = reverse('genre_info', kwargs={'id': 1})

    def get_object_dict(self, item):
        return dict(description=item['description'])

    def get_assertion_dict(self, object):
        return {
            'url': reverse('genre_info', kwargs={'id': object.id},
                prefix='http://testserver/'),
            }