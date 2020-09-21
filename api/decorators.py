from django.http import HttpResponse, JsonResponse

def require_login(view_func):
    
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            response = {"error": "Not logged in!"}
            return HttpResponse(JsonResponse(response), content_type="application/json", status=401)

    return wrapper