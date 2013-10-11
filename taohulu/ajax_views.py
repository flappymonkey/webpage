#encoding=utf8

import simplejson as json
from django.http import HttpResponse
from pymongo import json_util
from webpage.db_models.feeds import Feeds
from webpage.db_models.seckill import SecKill
from webpage.common.decorator import ajax_json_validate
from json_schema import *
import logging
from webpage.taohulu.dev import *
info_log = logging.getLogger('infolog')
stat_log = logging.getLogger('statlog')

@ajax_json_validate(ajax_add_worth_schema)
def ajax_add_worth(request):
    ret_dict = {'success':True, 'data': '' }
    id = request.json['id']
    Feeds.add_worth(id)
    add_dict={}
    add_dict['id'] = id
    add_dict['cid'] = request.COOKIES.get('cid','unknown')
    stat_log.info('addworth=%s'%json.dumps(dict(add_dict)))
    return HttpResponse(json.dumps(ret_dict, default=json_util.default), mimetype='application/javascript')

@ajax_json_validate(ajax_add_bad_schema)
def ajax_add_bad(request):
    ret_dict = {'success':True, 'data': '' }
    id = request.json['id']
    Feeds.add_bad(id)
    add_dict={}
    add_dict['id'] = id
    add_dict['cid'] = request.COOKIES.get('cid','unknown')
    stat_log.info('addbad=%s'%json.dumps(dict(add_dict)))
    return HttpResponse(json.dumps(ret_dict, default=json_util.default), mimetype='application/javascript')

@ajax_json_validate(ajax_get_feeds_schema)
def ajax_get_feeds(request):
    ret_dict = {'success':True, 'data': '' }
    page_num = request.json['page_num']
    search_type = request.json['search_type']
    feeds = Feeds.get_all_feeds_ret_1(page_num,search_type)
    #info_log.info('get_feeds_num=%d,pg=%d,st=%d'%(len(feeds),page_num,search_type))
    #info_log.info('print ret_data is %s',feeds)
    stat_dict={}
    stat_dict['pn'] = page_num
    stat_dict['type'] = search_type
    stat_dict['cid'] = request.COOKIES.get('cid','unknown')
    stat_dict['ua'] = request.META.get('HTTP_USER_AGENT','unknown')
    stat_dict['ip'] = request.META.get('REMOTE_ADDR','unknown')
    stat_log.info('get_feed=%s'%json.dumps(dict(stat_dict)))
    ret_dict['data'] = feeds
    return HttpResponse(json.dumps(ret_dict, default=json_util.default), mimetype='application/javascript')

@ajax_json_validate(get_feeds_count_schema)
def get_feeds_count(request):
    ret_dict = {'success':True, 'data': '' }
    search_type = request.json['search_type']
    count = Feeds.get_feeds_count(search_type)
    ret_dict['data'] = count
    return HttpResponse(json.dumps(ret_dict, default=json_util.default), mimetype='application/javascript')
@ajax_json_validate(ajax_get_seckills_schema)
def ajax_get_seckills(request):
    ret_dict = {'success':True, 'data': '' }
    req_type = request.json['req_type']
    order = request.json['order']
    page_num = request.json['page_num']
    seckills = SecKill.get_return_list(req_type,order,page_num)
    stat_dict={}
    stat_dict['pn'] = page_num
    stat_dict['type'] = req_type
    stat_dict['order'] = order
    stat_dict['cid'] = request.COOKIES.get('cid','unknown')
    stat_dict['ua'] = request.META.get('HTTP_USER_AGENT','unknown')
    stat_dict['ip'] = request.META.get('REMOTE_ADDR','unknown')
    stat_log.info('get_seckills=%s'%json.dumps(dict(stat_dict)))
    ret_dict['data'] = seckills
    return HttpResponse(json.dumps(ret_dict, default=json_util.default), mimetype='application/javascript')

@ajax_json_validate(get_seckills_count_schema)
def get_seckills_count(request):
    ret_dict = {'success':True, 'data': '' }
    count = SecKill.get_seckills_count()
    ret_dict['data'] = count
    return HttpResponse(json.dumps(ret_dict, default=json_util.default), mimetype='application/javascript')