__author__ = 'gaonan'

import logging
import simplejson as json
from django.conf import  settings
from djangomako.shortcuts import  render_to_response
from django.http import Http404

info_log = logging.getLogger('infolog')

class ExceptionMiddleware(object):
    UNKNOWN_INTERNAL_ERROR = "unknown internal server error!"
    def process_exception(self, request, exception):
        cookie = request.COOKIES.get('cid','unknown')
        str = '\nEXCEPTION_cookie:%s\npath:%s\nPOST%s\nGET:%s\nUSER_AGENT:%s\nHTTP_REFERER:%s'%(cookie,request.path,request.POST,request.GET,request.META['HTTP_USER_AGENT'],request.META.get('HTTP_REFERER',None))
        if isinstance(exception, Http404):
            info_log.exception(str)
            return None
        if request.is_ajax():
            info_log.exception(str)
        else:
            if not settings.DEBUG:
                info_log.exception(str)
                rsp = render_to_response('500.html', {}, context_instance=RequestContext(request))
                rsp.status_code = 500
                return rsp
            else:
                return None