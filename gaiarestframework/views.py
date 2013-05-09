from djangorestframework.mixins import ReadModelMixin, DeleteModelMixin
from djangorestframework.permissions import IsUserOrIsAnonReadOnly
from djangorestframework.views import ModelView
from gaiarestframework.mixins import *

__all__ = (
    'GaiaListOrCreateModelView',
    'GaiaInstanceModelView',
    'AuthGaiaListOrCreateModelView',
    'AuthGaiaInstanceModelView',
)


class GaiaListOrCreateModelView(GaiaPaginatorMixin, GaiaListModelMixin, GaiaCreateModelMixin, ModelView):
    _suffix = 'List'


class GaiaInstanceModelView(ReadModelMixin, GaiaUpdateModelMixin, DeleteModelMixin, ModelView):
    _suffix = 'Instance'


class AuthGaiaListOrCreateModelView(GaiaListOrCreateModelView):
    permissions = (IsUserOrIsAnonReadOnly, )


class AuthGaiaInstanceModelView(GaiaInstanceModelView):
    permissions = (IsUserOrIsAnonReadOnly, )
