from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the budget index.")


def import_csv(request):
    response = "This is the import screen"
    return render(request, "import.html", {})
    # return HttpResponse(response)
