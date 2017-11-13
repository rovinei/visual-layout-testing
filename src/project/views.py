from __future__ import unicode_literals
from django.shortcuts import redirect, render
from django.http import HttpResponseBadRequest


def redirect_view(request):
    if request.method == 'GET':
        return redirect('/admin/login/?next=/automate/')
    else:
        return HttpResponseBadRequest()
