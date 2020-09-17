from django.http import HttpResponseForbidden, JsonResponse

def require_login(view_func):
    
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            response = {"error": "Not logged in!"}
            return HttpResponseForbidden(JsonResponse(response), content_type="application/json")

    return wrapper