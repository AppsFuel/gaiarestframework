from django.core.exceptions import FieldError
from djangorestframework import status
from djangorestframework.mixins import *
from djangorestframework.response import ErrorResponse
from gaiarestframework.settings import GAIA_PAGINATOR_LIMIT

__all__ = (
    'GaiaListModelMixin',
    'GaiaCreateModelMixin',
    'GaiaUpdateModelMixin',
    'GaiaPaginatorMixin',
)


QP_RESERVED = ('limit', 'page')


def _t(k, v):
    if k.endswith('__in'):
        v = v.split(',')
    return k, v


class GaiaListModelMixin(ListModelMixin):
    def get_query_kwargs(self, request, *args, **kwargs):
        kwargs.update([_t(k, v) for k, v in request.GET.items() if k not in QP_RESERVED])
        return super(GaiaListModelMixin, self).get_query_kwargs(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            ordering = self.get_ordering()
            query_kwargs = self.get_query_kwargs(request, *args, **kwargs)

            for key, value in query_kwargs.copy().iteritems():
                if key.endswith('__md5'):
                    attribute, _ = key.split('__')
                    queryset = queryset.extra(where=["MD5(\"{0}\") = \"{1}\"".format(attribute, value)])
                    del query_kwargs[key]

            queryset = queryset.filter(**query_kwargs)
            if ordering:
                queryset = queryset.order_by(*ordering)

            return queryset
        except FieldError as e:
            raise ErrorResponse(status.HTTP_400_BAD_REQUEST, {'detail': '%s' % e})


def set_data_from_path(view, **kwargs):
    pk_name = view._resource.model._meta.pk.name
    form_fields = view._resource.get_bound_form().fields
    fields = [field for field in form_fields if field != pk_name]
    model_fields = [field.name for field in view._resource.model._meta.fields]
    if view._data is not None:
        view._data = dict(view._data.items())
        for key, value in kwargs.items():
            if key in fields:
                view._data[key] = value
                del kwargs[key]
    view.CONTENT  # !
    for field in set(fields) - set(model_fields):
        del view._content[field]
    return kwargs


class GaiaCreateModelMixin(CreateModelMixin):
    def post(self, request, *args, **kwargs):
        kwargs = set_data_from_path(self, **kwargs)
        resp = super(GaiaCreateModelMixin, self).post(request, *args, **kwargs)
        resp.raw_content = self.resource.model.objects.get(pk=resp.raw_content.pk)
        return resp


class GaiaUpdateModelMixin(UpdateModelMixin):
    def put(self, request, *args, **kwargs):
        query_kwargs = self.get_query_kwargs(request, **kwargs)
        self.model_instance = self.get_instance(**query_kwargs)
        kwargs = set_data_from_path(self, **kwargs)
        resp = super(GaiaUpdateModelMixin, self).put(request, *args, **kwargs)
        return self.resource.model.objects.get(pk=resp.pk)

    def get_instance(self, **kwargs):
        try:
            return super(GaiaUpdateModelMixin, self).get_instance(**kwargs)
        except self.resource.model.DoesNotExist:
            raise ErrorResponse(status.HTTP_404_NOT_FOUND)


class GaiaPaginatorMixin(PaginatorMixin):
    limit = GAIA_PAGINATOR_LIMIT

    def url_with_page_number(self, page_number):
        return self.request.build_absolute_uri(
            super(GaiaPaginatorMixin, self).url_with_page_number(page_number)
        )

    def get_limit(self):
        try:
            limit = int(self.request.GET.get('limit', self.limit))
        except ValueError:
            raise ErrorResponse(status.HTTP_400_BAD_REQUEST)
        if limit <= 0:
            raise ErrorResponse(status.HTTP_400_BAD_REQUEST)
        return min(limit, self.limit)
