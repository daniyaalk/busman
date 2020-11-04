from django.shortcuts import redirect

class UserHasNoOrganizationMixin:
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.info.has_organization() == False:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('org-dash')
