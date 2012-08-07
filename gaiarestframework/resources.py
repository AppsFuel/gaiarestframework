from djangorestframework.resources import ModelResource

__all__ = ('GaiaModelResource',)


class GaiaModelResource(ModelResource):
    include = ('url',)

    def url(self, item):
        return self.request.build_absolute_uri(item.get_absolute_url())
