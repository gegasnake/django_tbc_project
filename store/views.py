from django.http import HttpResponse


def store_home(request):
    return HttpResponse("Welcome to the Store!")


def product_list(request):
    return HttpResponse("List of Products")
