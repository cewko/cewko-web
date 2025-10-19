from django.shortcuts import render
from django.http import Http404


def home(request):
    return render(request, "pages/home.html")

def about(request):
    raise Http404("Coming soon")

def custom_404(request, exception):
    return render(request, "pages/404.html", status=404)