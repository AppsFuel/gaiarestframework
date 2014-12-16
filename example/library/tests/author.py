import json
from django.db import DatabaseError
from django.core.urlresolvers import reverse
from django.utils import unittest
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

    def test__md5(self):
        try:
            resp = self.client.get(self.resource_list_path + '?name__md5=dad5840ce44580d3a549fa326e104704')
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content, '')
        except DatabaseError:  # SQLITE3
            raise unittest.SkipTest()


