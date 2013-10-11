#encoding=utf8
"""doc string for module"""
__author__ = 'shenb shenbin@maimiaotech.com'

import sys
import logging
import traceback
import inspect
from time import  sleep
from datetime import datetime
from django.http import HttpResponseBadRequest
import simplejson as json
from validictory import  ValidationError
from validictory import  validate
from pymongo.errors import AutoReconnect, OperationFailure, PyMongoError

from webpage.common.exceptions import  InvalidInputException
from webpage.common.exceptions import  MongodbException

logger = logging.getLogger(__name__)

def ajax_json_validate(schema):
    """
    Validate the request's JSON input and make the deserialized data available
    under ``request.json`` before calling the decorated view.

    raise ``InvalidException`` on error.

    It will ensure:
    - request is a ajax request
    - JSON input (request.body) validates against the given JSON ``schema``

    json schema draft: http://tools.ietf.org/html/draft-zyp-json-schema-03
    json schema validator plugin: https://github.com/sunlightlabs/validictory

    """

    def _decorator(view_func):

        def _wrapper_view(request, *args, **kwargs):
            if not request.is_ajax:
                return HttpResponseBadRequest("the request should be a ajax call",
                    mimetype='application/javascript')
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError,e:
                import traceback
                traceback.print_exc()
                raise InvalidInputException(repr(e))

            try:
                validate(data, schema)
            except ValidationError, e:
                raise InvalidInputException(repr(e))

            request.json = data
            return view_func(request, *args, **kwargs)
        return _wrapper_view

    return _decorator


def mongo_exception(func):
    """
    decorator to catch and deal with mongodb exception in a uniform way.

    example:
    if AutoReconnect exception occurs, we will catch it and retry the last mongodb operation.

    NOTICE:
    this  decorator can be only used for **transaction**, if not, data maybe in a mess.

    """
    MAX_RETRY_TIMES = 40
    def wrapped_func(*args, **kwargs):
        retry_times = 0
        while True:
            try:
                return func(*args, **kwargs)
            except AutoReconnect, e:
                retry_times += 1
                if retry_times >= MAX_RETRY_TIMES:
                    logging.exception("retry but still got an AutoReconnect exception when operate on mongodb")
                    raise MongodbException(msg=e)
                sleep(10)

            except  OperationFailure, e:
                logging.exception("got an exception when operate on mongodb")
                raise MongodbException(msg=e)

            except PyMongoError,e:
                logging.exception("got an exception when operate on mongodb")
                raise MongodbException(msg=e)

    return wrapped_func
