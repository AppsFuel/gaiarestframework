from urlobject import URLObject
from djangorestframework.mixins import *

__all__ = (
    'GaiaListModelMixin',
    'GaiaCreateModelMixin',
    'GaiaUpdateModelMixin',
    'GaiaPaginatorMixin',
)


QP_RESERVED = ('limit', 'page')


class GaiaListModelMixin(ListModelMixin):
    def get_query_kwargs(self, request, *args, **kwargs):
        kwargs.update([(str(k), v) for k, v in request.GET.items() if k not in QP_RESERVED])
        return super(GaiaListModelMixin, self).get_query_kwargs(request, *args, **kwargs)


def set_data_from_path(view, **kwargs):
    fields = view._resource.get_bound_form().fields
    view._data = dict(view._data.items())

    for key, value in kwargs.items():
        if key in fields:
            view._data[key] = value
            del kwargs[key]
    return kwargs


class GaiaCreateModelMixin(CreateModelMixin):
    def post(self, request, *args, **kwargs):
        kwargs = set_data_from_path(self, **kwargs)
        resp = super(GaiaCreateModelMixin, self).post(request, *args, **kwargs)
        resp.raw_content = self.resource.model.objects.get(pk=resp.raw_content.pk)
        return resp


class GaiaUpdateModelMixin(UpdateModelMixin):
    def put(self, request, *args, **kwargs):
        kwargs = set_data_from_path(self, **kwargs)
        resp = super(GaiaUpdateModelMixin, self).put(request, *args, **kwargs)
        return self.resource.model.objects.get(pk=resp.pk)


class GaiaPaginatorMixin(PaginatorMixin):
    def url_with_page_number(self, page_number):
        url = URLObject(self.request.build_absolute_uri())
        url = url.set_query_param('page', str(page_number))
        limit = self.get_limit()
        if limit != self.limit:
            url = url.set_query_param('limit', str(limit))
        return url
