from djangorestframework.mixins import ReadModelMixin, DeleteModelMixin, PaginatorMixin
from djangorestframework.permissions import IsAuthenticated
from djangorestframework.views import ModelView
from gaiarestframework.mixins import *

__all__ = (
    'GaiaListOrCreateModelView',
    'GaiaInstanceModelView',
    'AuthGaiaListOrCreateModelView',
    'AuthGaiaInstanceModelView',
)


class GaiaListOrCreateModelView(PaginatorMixin, GaiaListModelMixin, GaiaCreateModelMixin, ModelView):
    _suffix = 'List'


class GaiaInstanceModelView(ReadModelMixin, GaiaUpdateModelMixin, DeleteModelMixin, ModelView):
    _suffix = 'Instance'


class AuthGaiaListOrCreateModelView(GaiaListOrCreateModelView):
    permissions = (IsAuthenticated, )


class AuthGaiaInstanceModelView(GaiaInstanceModelView):
    permissions = (IsAuthenticated, )
