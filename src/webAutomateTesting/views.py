from __future__ import unicode_literals
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest


def redirect_view(request):
    if request.method == 'GET':
        return redirect('/admin/')
    else:
        return HttpResponseBadRequest()
