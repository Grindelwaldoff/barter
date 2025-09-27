from django.shortcuts import render


def page_not_found(request, exception):
    return render(
        request,
        'core/404.html',
        {'path': request.path},
        status=404
    )


def csrf_failure(request, reason='', exception=None):
    return render(request, 'core/403csrf.html', status=403)


def server_failure(request):
    return render(request, 'core/500.html')
