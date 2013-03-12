from django.core.urlresolvers import reverse
from gaiarestframework import testutils
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

    def get_assertion_dict(self, obj):
        return {
            'url': testutils.reverse('author_info', kwargs={'id': obj.id}),
        }

