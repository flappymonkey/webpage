#encoding=utf8

import sys
import os
import json
import urllib2
import datetime
import logging
import random
import hashlib
import hmac
import time

from webpage.taohulu.dev import *
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from djangomako.shortcuts import render_to_response
from webpage.db_models.feeds import Feeds
from webpage.db_models.seckill import SecKill
from django.views.decorators.csrf import  ensure_csrf_cookie
from webpage.common.openqqpy import OpenQQClient
from webpage.db_models.userinfo import UserInfo
from webpage.qquser_models.get_info import QQUsereInfo
from webpage.taohulu.settings import APP_ID,APP_KEY,REDIRECT_URI,SCOPE
from webpage.taohulu.settings import TAOBAO_APP_KEY,TAOBAO_APP_SECRET

info_log = logging.getLogger('infolog')
stat_log = logging.getLogger('statlog')

@ensure_csrf_cookie
def home(request):
    (top_feeds,common_feeds) = Feeds.get_all_feeds_ret_2(1,0)
    userinfo = None
    open_id = get_cookie(request,'od')
    if open_id:
        userinfo = UserInfo.get_user_info_by_openid(open_id)
    response = render_to_response("index.html",{'top_feeds': top_feeds, 'common_feeds': common_feeds, 'userinfo': userinfo}, context_instance=RequestContext(request))

    stat_dict={}
    stat_dict['pn'] = 1
    stat_dict['type'] = 0
    if get_cookie(request,'cid'):
        cid = get_cookie(request,'cid')
        info_log.info('cookie %s coming'%cid)
        stat_dict['cid'] = cid
        stat_dict['ua'] = request.META.get('HTTP_USER_AGENT','unknown')
        stat_dict['ip'] = request.META.get('REMOTE_ADDR','unknown')
        stat_log.info('get_home=%s'%json.dumps(dict(stat_dict)))
    else:
        cid = create_cookie_id(request)
        set_cookie(response,'cid',cid)
        info_log.info('create cookie id %s'%cid)
        stat_dict['cid'] = cid
        stat_dict['ua'] = request.META.get('HTTP_USER_AGENT','unknown')
        stat_dict['ip'] = request.META.get('REMOTE_ADDR','unknown')
        stat_log.info('get_home=%s'%json.dumps(dict(stat_dict)))
    return response

@ensure_csrf_cookie
def seckill(request):

    if 'req_type' in request.GET and request.GET['req_type'].isdigit():
        req_type = int(request.GET['req_type'])
    else:
        req_type = 3
    order = 1
    page_num = 1
    sec_kills = SecKill.get_return_list(req_type,order,page_num)
    userinfo = None
    open_id = get_cookie(request,'od')
    if open_id:
        userinfo = UserInfo.get_user_info_by_openid(open_id)
    response = render_to_response("seckill.html",{'sec_kills': sec_kills, 'userinfo': userinfo, 'req_type': req_type}, context_instance=RequestContext(request))

    stat_dict={}
    stat_dict['pn'] = 1
    stat_dict['type'] = 0
    if get_cookie(request,'cid'):
        cid = get_cookie(request,'cid')
        info_log.info('cookie %s coming'%cid)
        stat_dict['cid'] = cid
        stat_dict['ua'] = request.META.get('HTTP_USER_AGENT','unknown')
        stat_dict['ip'] = request.META.get('REMOTE_ADDR','unknown')
        stat_log.info('get_seckill_home=%s'%json.dumps(dict(stat_dict)))
    else:
        cid = create_cookie_id(request)
        set_cookie(response,'cid',cid)
        info_log.info('create cookie id %s'%cid)
        stat_dict['cid'] = cid
        stat_dict['ua'] = request.META.get('HTTP_USER_AGENT','unknown')
        stat_dict['ip'] = request.META.get('REMOTE_ADDR','unknown')
        stat_log.info('get_seckill_home=%s'%json.dumps(dict(stat_dict)))
    return response

def goldmall(request):
    userinfo = None
    open_id = get_cookie(request,'od')
    if open_id:
        userinfo = UserInfo.get_user_info_by_openid(open_id)
    return render_to_response("goldmall.html",{'userinfo': userinfo}, context_instance=RequestContext(request))

def redirect(request):
    if request.method == 'GET':
        clk_dict = create_clk_dict(request)
        if 'show_type' in clk_dict and clk_dict['show_type'] == 1:
            show_type = 1
        else:
            show_type = 0

        if show_type == 1:
            item = SecKill.get_seckill_link_by_id(clk_dict['link_id'])

        else:
            item = Feeds.get_feed_url_by_linkid(clk_dict['link_id'])
        if item:
            if show_type == 1:
                clk_dict['real_link'] = add_link_id(item['link'])
            else:
                clk_dict['real_link'] = item['link']
            stat_log.info('clk=%s'%json.dumps(dict(clk_dict)))
            response = render_to_response("redirect.html",{'id': clk_dict['feed_id'], 'url': clk_dict['real_link']}, context_instance=RequestContext(request))

            timestamp = str(int(time.time())) + '000'
            message = TAOBAO_APP_SECRET + 'app_key' + TAOBAO_APP_KEY + 'timestamp' + timestamp + TAOBAO_APP_SECRET
            mysign = hmac.new(TAOBAO_APP_SECRET)
            mysign.update(message)
            mysign = mysign.hexdigest().upper()
            set_cookie(response,'timestamp',timestamp)
            set_cookie(response,'sign',mysign)
            
            return response
        else:
            info_log.info('invalid clk url %s'%clk_dict)
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def login(request):
    if request.method == 'GET' and 'code' in request.GET:
        code = request.GET['code']
        client = OpenQQClient(client_id=APP_ID,client_secret=APP_KEY,redirect_uri=REDIRECT_URI,scope=SCOPE)
        access_token = client.request_access_token(code)
        client.set_access_token(access_token['access_token'],access_token['expires_in'])
        open_id = client.request_openid()
        client.set_openid(open_id)
        info_log.info('get a_token:%s exp:%s open_id:%s'%(access_token['access_token'],access_token['expires_in'],open_id))
        #response = render_to_response("index.html",{'top_feeds': top_feeds, 'common_feeds': common_feeds}, context_instance=RequestContext(request))
        response = HttpResponseRedirect('/')
        set_cookie(response,'at',access_token['access_token'],cookie_max_age=access_token['exp_time'])
        set_cookie(response,'od',open_id,cookie_max_age=access_token['exp_time'])
        set_cookie(response,'ep',access_token['expires_in'],cookie_max_age=access_token['exp_time'])
        user_info = QQUsereInfo.get_user_info(client)
        info_log.info('get userinfo from qq')
        weibo_info = QQUsereInfo.get_weibo_info(client)
        info_log.info('get weiboinfo from qq')
        info_log.info('info openid:%s user_info:%s'%(open_id,user_info))
        info_log.info('winfo openid:%s user_info:%s'%(open_id,weibo_info))
        UserInfo.save_user_info_by_openid(open_id,user_info)
        info_log.info('save userinfo to db')
        UserInfo.save_user_weibo_info_by_openid(open_id,weibo_info)
        info_log.info('save weibo to db')
        return response
    else:
        return HttpResponseRedirect('/')

def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('od')
    return response

def my_404_view(request):
    #logger.info("[action] sid:%s reach 404 page"%(request.dbname,))
    response = render_to_response('404.html',{}, context_instance=RequestContext(request))
    response.status_code = 404
    return response

def my_500_view(request):
    #logger.info("[action] sid:%s reach 500 page"%(request.dbname,))
    response =  render_to_response('500.html',{}, context_instance=RequestContext(request))
    response.status_code = 500
    return response