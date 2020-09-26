from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from .decorators import require_login

# Create your views here.
@require_login
def home(request):
    response = {"message": f"Hi, {request.user}!"}
    return JsonResponse(response)

class CategoryAutocomplete(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        term = request.GET['term']
        response = set(Product.objects.filter(organization=request.user.organization,
                                              category__icontains=term).values_list('category', flat=True).distinct())
        return Response(response)

class NameAutocomplete(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        term = request.GET['term']
        response = set(Product.objects.filter(organization=request.user.organization,
                                            name__icontains=term).values_list('name', flat=True).distinct())
        return Response(response)


class BrandAutocomplete(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        term = request.GET['term']
        response = set(Product.objects.filter(organization=request.user.organization,
                                              name__icontains=term).values_list('brand', flat=True).distinct())
        return Response(response)
