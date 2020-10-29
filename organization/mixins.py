from django.http import HttpResponseNotAllowed

class UserHasNoGroupMixin:
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.count() == 0:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed("a")