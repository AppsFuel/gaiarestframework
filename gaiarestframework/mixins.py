from djangorestframework.mixins import *
from gaiarestframework.settings import GAIA_PAGINATOR_LIMIT

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
    pk_name = view._resource.model._meta.pk.name
    form_fields = view._resource.get_bound_form().fields
    fields = [field for field in form_fields if field != pk_name]
    model_fields = [field.name for field in view._resource.model._meta.fields]
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
        kwargs = set_data_from_path(self, **kwargs)
        resp = super(GaiaUpdateModelMixin, self).put(request, *args, **kwargs)
        return self.resource.model.objects.get(pk=resp.pk)


class GaiaPaginatorMixin(PaginatorMixin):
    limit = GAIA_PAGINATOR_LIMIT

    def url_with_page_number(self, page_number):
        return self.request.build_absolute_uri(
            super(GaiaPaginatorMixin, self).url_with_page_number(page_number)
        )
