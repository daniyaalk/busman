from django.http.response import HttpResponseNotAllowed
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Permissions

class PermissionsHandlerMixin:

    def dispatch(self, request, *args, **kwargs):
        #Skip tests if user is the owner
        if hasattr(self.request.user, 'organization'):
            return super().dispatch(request, *args, **kwargs)
        
        #Return Access denied if no permissions found
        elif not hasattr(self.request.user, 'permissions'):
            return HttpResponseNotAllowed("Not Allowed")

        elif hasattr(self, 'permissions_required') and hasattr(self, 'permissions_level'):
            for i, permission in enumerate(self.permissions_required):
                    if getattr(self.request.user.permissions, permission) < self.permissions_level[i]:
                        return HttpResponseNotAllowed("Not Allowed")

        return super().dispatch(request, *args, **kwargs)
