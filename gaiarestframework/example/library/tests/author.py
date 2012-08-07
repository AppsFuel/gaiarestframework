from gaiarestframework import testutils
from django.core.urlresolvers import reverse
from example.library.models import Author

class AuthorTestCase(testutils.GaiaTestCase):
    fixtures = ['user.json', 'author.json', ]
    resource_cls = Author
    resource = {'name': 'dante', 'surname': 'alighieri'}
    resource_list_path = reverse('author_list')
    resource_instance_path = reverse('author_info', kwargs={'id': 1})

    def get_object_dict(self, item):
        return {
            'name': item['name'],
            'surname': item['surname'],
        }

    def get_assertion_dict(self, object):
        return {
            'url': reverse('author_info', kwargs={'id': object.id},
                prefix='http://testserver/'),
        }

