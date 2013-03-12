from gaiarestframework import testutils
from django.core.urlresolvers import reverse
from example.library.models import Genre


class GenreListTestCase(testutils.GaiaAuthTestCase):
    fixtures = ['user.json', 'genre.json', ]
    resource_cls = Genre
    resource = {'description': 'Thriller', 'toremove': True}
    resource_list_path = reverse('genre_list')
    resource_instance_path = reverse('genre_info', kwargs={'description': 'Fantasy'})

    def get_object_dict(self, item):
        return dict(description=item['description'])

    def get_assertion_dict(self, obj):
        return {
            'url': testutils.reverse('genre_info', kwargs={'description': obj.pk}),
        }