# -*- coding: utf-8 -*-
import threading
from django.core.handlers.wsgi import WSGIRequest
from django.utils.deprecation import MiddlewareMixin

from request_provider.signals import request_accessor


_thread_locals = threading.local()


class RequestProviderError(Exception):
    pass


class RequestProvider(MiddlewareMixin):

    def __init__(self, get_response=None):
        super(RequestProvider, self).__init__(get_response)
        _thread_locals.request_provier_request = None
        request_accessor.connect(self)

    def process_request(self, request):
        _thread_locals.request_provier_request = request
        return None

    def __call__(self, *args, **kwargs):
        if 'signal' in kwargs:
            return _thread_locals.request_provier_request
        return super(RequestProvider, self).__call__(*args, **kwargs)
