from django.core.exceptions import PermissionDenied
from .models import Permissions

class PermissionsHandlerMixin:

    def dispatch(self, request, *args, **kwargs):

        if hasattr(self, 'permissions_required') and hasattr(self, 'permissions_level'):

            for i, permission in enumerate(self.permissions_required):
                is_owner = hasattr(self.request.user, 'organization')
                if not is_owner and getattr(self.request.user.permissions, permission) < self.permissions_level[i]:
                    raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

