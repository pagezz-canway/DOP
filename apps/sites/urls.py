# -*- coding: utf-8 -*-
from django.conf.urls import url

from apps.sites.views import index

urlpatterns = [
    url(r'^$', index),
]
