# -*- coding: utf-8 -*-
from django.core.handlers.wsgi import WSGIRequest
from django.utils.deprecation import MiddlewareMixin

from request_provider.signals import request_accessor


class RequestProviderError(Exception):
    pass


class RequestProvider(MiddlewareMixin):

    def __init__(self, get_response=None):
        super(RequestProvider, self).__init__(get_response)
        self._request = None
        request_accessor.connect(self)

    def process_request(self, request):
        self._request = request
        return None

    def __call__(self, *args, **kwargs):
        if 'signal' in kwargs:
            return self._request
        return super(RequestProvider, self).__call__(*args, **kwargs)
