from django.shortcuts import render
from django.views.decorators.cache import never_cache


@never_cache
def hangout_view(request):
    return render(request, "hangout/hangout.html")
