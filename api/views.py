from django.http import JsonResponse
from products.models import Product
from .decorators import require_login

# Create your views here.
@require_login
def home(request):
    response = {"message": f"Hi, {request.user}!"}
    return JsonResponse(response)

@require_login
def categoryAutoComplete(request):
    term = request.GET['term']
    response = set(Product.objects.filter(organization=request.user.organization, category__icontains=term).values_list('category', flat=True).distinct())
    return JsonResponse(list(response), safe=False)


@require_login
def nameAutoComplete(request):
    term = request.GET['term']
    response = set(Product.objects.filter(organization=request.user.organization,
                                           name__icontains=term).values_list('name', flat=True).distinct())
    return JsonResponse(list(response), safe=False)


@require_login
def brandAutoComplete(request):
    term = request.GET['term']
    response = set(Product.objects.filter(organization=request.user.organization,
                                           brand__icontains=term).values_list('brand', flat=True).distinct())
    return JsonResponse(list(response), safe=False)
