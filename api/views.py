from django.http import HttpResponseForbidden, JsonResponse
from products.models import Product

# Create your views here.
def home(request):
    
    if request.user.is_authenticated:
        response = {"message": f"Hi, {request.user}!"}
        return HttpResponseForbidden(JsonResponse(response), content_type="application/json")
    else:
        response = {"error": "Not Logged In!"}
        return HttpResponseForbidden(JsonResponse(response), content_type="application/json")


def categoryAutoComplete(request):

    if request.user.is_authenticated:
        term = request.GET['term']
        response = list(Product.objects.filter(organization=request.user.organization, category__contains=term).values_list('category', flat=True))
        print(response)
        return JsonResponse(response, safe=False)
    else:
        response = {"error": "Not Logged In!"}
        return HttpResponseForbidden(JsonResponse(response), content_type="application/json")
