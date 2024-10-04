from django.http import HttpResponse


def order_home(request):
    return HttpResponse("Order Home")


def order_details(request):
    return HttpResponse("Order Details")
