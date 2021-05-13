# -*- coding: utf-8 -*-
from .default import *  # noqa

BKDATA_URL = f"{os.getenv('BK_PAAS_HOST', '')}/t/bk_dataweb"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bk_dop',
        'USER': 'paas',
        'PASSWORD': '57puTyrEuGsB',
        'HOST': 'mysql-paas.service.consul',
        'PORT': '3306',
    },
}
