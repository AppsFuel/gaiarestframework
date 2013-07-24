import functools
import json
from math import ceil
from urlparse import urljoin
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse as django_reverse, resolve
from django.test import TestCase
from django.utils import unittest
from gaiarestframework.settings import GAIA_PAGINATOR_LIMIT
from gaiarestframework import mixins
json_datetime = lambda dt: DjangoJSONEncoder().default(dt)


def reverse(viewname, urlconf=None, args=None, kwargs=None, prefix=None, current_app=None):
    return urljoin(
        'http://testserver',
        django_reverse(viewname, urlconf, args, kwargs, prefix, current_app)
    )


class TestNeed(object):
    def __init__(self, _type, *mixins):
        self._type = 'view_{0}_cls'.format(_type)
        self.mixins = mixins

    def __call__(self, f):
        @functools.wraps(f)
        def wrapper(*args):
            for mixin in self.mixins:
                if not issubclass(getattr(args[0], self._type), mixin):
                    return lambda x: x
            return f
        return wrapper


class NeedUpdate(TestNeed):
    def __init__(self):
        super(NeedUpdate, self).__init__('instance', mixins.GaiaUpdateModelMixin)


class NeedDelete(TestNeed):
    def __init__(self):
        super(NeedDelete, self).__init__('instance', mixins.DeleteModelMixin)


class NeedCreate(TestNeed):
    def __init__(self):
        super(NeedCreate, self).__init__('list', mixins.GaiaCreateModelMixin)



class GaiaTestCase(TestCase):
    resource_cls = NotImplemented
    resource = NotImplemented
    resource_list_path = NotImplemented
    resource_instance_path = NotImplemented
    antidupe = True

    @property
    def resource_update(self):
        return self.resource

    @property
    def view_instance_cls(self):
        return resolve(self.resource_instance_path).func.cls_instance.__class__

    @property
    def view_list_cls(self):
        return resolve(self.resource_list_path).func.cls_instance.__class__

    def testReadNotFound(self):
        self.resource_cls.objects.all().delete()
        resp = self.client.get(self.resource_instance_path)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.content, '')

    @NeedUpdate()
    def testUpdateNotFound(self):
        self.resource_cls.objects.all().delete()
        resp = self.client.put(self.resource_instance_path, content_type='application/json')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.content, '')

    @NeedDelete()
    def testDeleteNotFound(self):
        self.resource_cls.objects.all().delete()
        resp = self.client.delete(self.resource_instance_path, content_type='application/json')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.content, '')

    def testListContentPaginationBadLimit(self):
        resp = self.client.get(self.resource_list_path + '?limit=0')
        self.assertEqual(resp.status_code, 400)
        resp = self.client.get(self.resource_list_path + '?limit=-1')
        self.assertEqual(resp.status_code, 400)
        resp = self.client.get(self.resource_list_path + '?limit=str')
        self.assertEqual(resp.status_code, 400)

    def testReadStatus(self):
        resp = self.client.get(self.resource_list_path)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(self.resource_instance_path)
        self.assertEqual(resp.status_code, 200)

    def testListContentPagination(self):
        resp = self.client.get(self.resource_list_path)
        content = json.loads(resp.content)
        count = self.resource_cls.objects.count()
        pages = int(ceil(count / 20.0))
        self.assertEqual(content['page'], 1)
        self.assertEqual(content['next'], 'http://testserver' + self.resource_list_path + '?page=3' if pages > 1 else None)
        self.assertEqual(content['per_page'], GAIA_PAGINATOR_LIMIT)
        self.assertEqual(content['total'], count)
        self.assertEqual(content['pages'], pages)
        self.assertEqual(content['previous'], None)

    def testListContentPaginationLimit(self):
        resp = self.client.get(self.resource_list_path + '?limit=1&page=2')
        content = json.loads(resp.content)
        count = self.resource_cls.objects.count()
        self.assertEqual(content['page'], 2)
        self.assertEqual(content['next'], 'http://testserver' + self.resource_list_path + '?page=3&limit=1')
        self.assertEqual(content['per_page'], 1)
        self.assertEqual(content['total'], count)
        self.assertEqual(content['pages'], count)
        self.assertEqual(content['previous'], 'http://testserver' + self.resource_list_path + '?page=1&limit=1')

    def testListContentResults(self):
        resp = self.client.get(self.resource_list_path)
        results = json.loads(resp.content)['results']
        for item in results:
            self.assertItem(item)

    def testListQSError(self):
        resp = self.client.get(self.resource_list_path + '?1__like=er')
        self.assertEqual(resp.status_code, 400)
        self.assertTrue('detail' in json.loads(resp.content))

    @NeedCreate()
    def testCreateStatus(self):
        resp = self.client.post(self.resource_list_path, data=self.resource)
        self.assertEqual(resp.status_code, 201)

    @NeedCreate()
    def testCreateContent(self):
        resp = self.client.post(self.resource_list_path, data=self.resource)
        item = json.loads(resp.content)
        self.assertItem(item)

    @NeedCreate()
    def testCreateEmptyStatus(self):
        resp = self.client.post(self.resource_list_path)
        self.assertEqual(resp.status_code, 400)

    @NeedCreate()
    def testCreateDupeStatus(self):
        self.client.post(self.resource_list_path, data=self.resource)
        resp = self.client.post(self.resource_list_path, data=self.resource)
        self.assertEqual(resp.status_code, 400 if self.antidupe else 201)

    def testDeleteNotAllowed(self):
        count = self.resource_cls.objects.count()
        resp = self.client.delete(self.resource_list_path)
        self.assertEqual(resp.status_code, 405)
        self.assertEqual(self.resource_cls.objects.count(), count)

    def testUpdateNotAllowed(self):
        resp = self.client.put(self.resource_list_path, content_type='application/json')
        self.assertEqual(resp.status_code, 405)

    def testReadContent(self):
        resp = self.client.get(self.resource_instance_path)
        item = json.loads(resp.content)
        self.assertItem(item)

    @NeedUpdate()
    def testUpdateStatus(self):
        resp = self.client.put(self.resource_instance_path, data=json.dumps(self.resource_update), content_type='application/json')
        self.assertEqual(resp.status_code, 200, resp.content)

    @NeedUpdate()
    def testUpdateContent(self):
        count = self.resource_cls.objects.count()
        resp = self.client.put(self.resource_instance_path, data=json.dumps(self.resource_update), content_type='application/json')
        item = json.loads(resp.content)
        self.assertItem(item)
        update_can_create = int(self.resource_cls._meta.pk.name in self.resource_update)
        self.assertEqual(self.resource_cls.objects.count(), count + update_can_create)

    @NeedUpdate()
    def testUpdateEmptyStatus(self):
        resp = self.client.put(self.resource_instance_path, content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    @NeedDelete()
    def testDeleteStatus(self):
        count = self.resource_cls.objects.count()
        resp = self.client.delete(self.resource_instance_path, content_type='application/json')
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(self.resource_cls.objects.count(), count - 1)

    def testCreateNotAllowed(self):
        resp = self.client.post(self.resource_instance_path)
        self.assertEqual(resp.status_code, 405)

    def get_object_dict(self, item):
        return {}

    def get_assertion_dict(self, obj):
        return {}

    def assertItem(self, item):
        obj = self.resource_cls.objects.get(**self.get_object_dict(item))
        for k, v in self.get_assertion_dict(obj).items():
            self.assertEqual(item[k], v)


class GaiaAuthTestCase(GaiaTestCase):
    def setUp(self):
        self.client.login(username='test', password='test')

    def testCreateForbiddenStatus(self):
        self.client.logout()
        resp = self.client.post(self.resource_list_path, data=self.resource)
        self.assertEqual(resp.status_code, 403)

    def testUpdateForbiddenStatus(self):
        self.client.logout()
        resp = self.client.put(self.resource_list_path, data=json.dumps(self.resource_update), content_type='application/json')
        self.assertEqual(resp.status_code, 403)

    def testDeleteForbiddenStatus(self):
        self.client.logout()
        resp = self.client.delete(self.resource_list_path, content_type='application/json')
        self.assertEqual(resp.status_code, 403)
