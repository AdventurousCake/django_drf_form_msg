from django.shortcuts import render

# Create your views here.


def core_auth(request):
    return render(request, 'core/auth_page.html')