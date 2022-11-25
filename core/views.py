from django.shortcuts import render

# Create your views here.


def core_auth(request):
    return render(request, 'core/auth_page.html')


def forbidden(request, exception):
    return render(request, 'misc/403.html', status=403)


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {"path": request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)