__author__ = 'gaonan'
#encoding=utf8
from ztmhs.zhs.settings import COOKIE_AGE,APP_ID,APP_KEY,REDIRECT_URI,SCOPE
import datetime
import random
import hashlib
import logging

info_log = logging.getLogger('infolog')

def is_chinese(uchar):
    '''''判断一个unicode是否是汉字'''
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    return False
def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar<=u'\u0039':
        return True
    return False
def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar<=u'\u005a')\
    or (uchar >= u'\u0061' and uchar<=u'\u007a'):
        return True
    return False
def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    return False

# gbk宽度可用于对齐，中文占两个字符位置
def gbkwordlen(u):
    if is_chinese(u):
        return 2
    return 1

# 计算文本显示宽度
def gbkwordslen(uw):
    i = 0
    for u in uw:
        i += gbkwordlen(u)
    return i

def trunc_word(uw, len):
    l = 0
    i = 1
    for u in uw:
        l += gbkwordlen(u)
        if l > len:
            return uw[:i-1]
        i += 1
    return uw

def set_cookie(response,key,value,cookie_max_age=COOKIE_AGE):
    response.set_cookie(key,value,max_age=cookie_max_age)

def get_cookie(request,key):
    if key in request.COOKIES:
        return request.COOKIES[key]
    else:
        return None
def create_cookie_id(request):
    cur_str = ''
    cur_str = cur_str + request.META.get('HTTP_USER_AGENT', 'unknown') + ';'
    cur_str = cur_str + request.META.get('REMOTE_ADDR', 'unknown') + ';'
    cur_str = cur_str + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ';'
    cur_str = cur_str + str(random.random())
    info_log.info('create cookie by str %s'%cur_str)
    return hashlib.md5(cur_str).hexdigest().upper()

def add_link_id(link):
    if 'amazon.cn' in link:
        items = link.split('/')
        item_id = items[-2]
        return link + 'ref=as_li_ss_tl?camp=536&creative=3132&creativeASIN=' + item_id + '&linkCode=as2&tag=zhenhuasuan-23'
    else:
        return link

def create_clk_dict(request):
    ret_dict = {}
    ret_dict['ua'] = request.META.get('HTTP_USER_AGENT','unknown')
    ret_dict['ip'] = request.META.get('REMOTE_ADDR','unknown')
    ret_dict['feed_id'] = request.GET.get('fd', 'unknown')
    ret_dict['link_id'] = request.GET.get('lk', 'unknown')
    ret_dict['page_num'] = request.GET.get('pg', 'unknown')
    ret_dict['index_num'] = request.GET.get('nm', 'unknown')
    ret_dict['search_type'] = request.GET.get('st', 'unknown')
    ret_dict['top_type'] = request.GET.get('tt', 'unknown')
    ret_dict['cookie_id'] = request.COOKIES.get('cid','unknown')

    if 'it' in request.GET:
        #seckill 点击
        ret_dict['clk_position'] = '1'
        ret_dict['show_type'] = 1
    else:
        #feeds 点击
        ret_dict['clk_position'] = request.GET.get('ct', 'unknown')
        ret_dict['show_type'] = 0
    return ret_dict

def change_link(link):
    pass