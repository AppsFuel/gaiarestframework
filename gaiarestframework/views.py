from djangorestframework.mixins import ReadModelMixin, DeleteModelMixin, PaginatorMixin
#from djangorestframework.permissions import IsAuthenticated
from djangorestframework.views import ModelView
from gaiarestframework.mixins import *

__all__ = (
    'GaiaListOrCreateModelView',
    'GaiaInstanceModelView',
)


class GaiaListOrCreateModelView(PaginatorMixin, GaiaListModelMixin, GaiaCreateModelMixin, ModelView):
    _suffix = 'List'
    #permissions = (IsAuthenticated, )


class GaiaInstanceModelView(ReadModelMixin, GaiaUpdateModelMixin, DeleteModelMixin, ModelView):
    _suffix = 'Instance'
    #permissions = (IsAuthenticated, )
