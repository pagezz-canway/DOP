# -*- coding: utf-8 -*-
from django.shortcuts import render


def index(request):
    """首页"""

    return render(request, "index.html", {},)
