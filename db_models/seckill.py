__author__ = 'shen bin'
#encoding=utf8
import datetime
import time
from webpage.taohulu import settings
from webpage.taohulu.settings import SECKILL_PAGE_RET_NUM
from webpage.taohulu.settings import NO_PRICE_WAIT_TIME
from webpage.taohulu.dev import *

import logging
info_log = logging.getLogger('infolog')
class SecKill(object):
    """
    class to operate feeds
    """
    _conn = settings.mongoConn
    _db = "seckills"
    if _conn != None:
        seckills = _conn[_db]['seckill']
    else:
        seckills = None
    @classmethod
    def get_day_start_unix(cls):
        cur_str = datetime.datetime.now().strftime('%Y-%m-%d') + ' 00:00:00'
        return int(time.mktime(time.strptime(cur_str,'%Y-%m-%d %H:%M:%S')))

    #feed_id:id id link_id link id page:页号 num:第几位 item_type:1 seckill s_type：1 即将开始 2进行中 3价格排序 t_type 是否置顶
    @classmethod
    def create_link_flag(cls,id,link_id,page,num,item_type,s_type,t_type):
        return'fd=%s&lk=%s&pg=%d&nm=%d&it=%d&st=%d&tt=%d'%(id,link_id,page,num,item_type,s_type,t_type)
    @classmethod
    def get_return_list(cls,req_type,order,page_num):
        ret_list = []
        if not cls.seckills:
            return ret_list
        '''
            req_type 1:即将开始，2 进行中 3价格排序
            order 1正序，-1倒序
        '''
        arg_dict = { 1:[[1,1,1],[0,1,1],[1,2,1],[0,2,1],[1,3,1],[0,3,1]],
                     2:[[1,2,1],[0,2,1],[1,1,1],[0,1,1],[1,3,1],[0,3,1]],
                     3:[[1,2,2],[0,2,2],[1,1,1],[0,1,1],[1,3,1],[0,3,1]]
        }

        if req_type < 1 or req_type > 3 or order != 1 and order != -1 or page_num < 1:
            return ret_list

        begin_time = cls.get_day_start_unix()
        end_time = begin_time + 86400
        current_time = int(time.time())
        skip_num = (page_num - 1) * SECKILL_PAGE_RET_NUM
        count = 0
        select_num = 0
        for i in range(0,6):
            up = arg_dict[req_type][i][0]
            stat = arg_dict[req_type][i][1]
            sort_type = arg_dict[req_type][i][2]
            cursor = cls.get_seckills(up,stat,sort_type,order,begin_time,end_time,current_time)
            #info_log.info('cur_count:%d idx:%d seckillscount:%d skip_num:%d'%(count,i,cursor.count(),skip_num))
            if count + cursor.count() > skip_num:
                for item in cursor:
                    if count >= skip_num:
                        if item['stat'] == 1 and item['display_time_begin'] < current_time:
                            item['stat'] = 2
                        item['link_id'] = cls.create_link_flag(item['id'],item['id'],page_num,select_num,1,req_type,up)
                        if gbkwordslen(item['title'].strip()) > 74:
                            item['title'] = trunc_word(item['title'].strip(),74) + u'...'
                        ret_list.append(item)
                        select_num += 1
                        if select_num == SECKILL_PAGE_RET_NUM:
                            return ret_list
                    else:
                        count += 1
            else:
                count += cursor.count()
        return ret_list
    @classmethod
    def get_seckills_count(cls):
        #begin_time = cls.get_day_start_unix()
        #end_time = begin_time + 86400
        #count = cls.seckills.find({'stat':{'$in':[1,2,3]},'display_time_begin':{"$gte":begin_time,"$lt":end_time}}).count()
        arg_dict = { 1:[[1,1,1],[0,1,1],[1,2,1],[0,2,1],[1,3,1],[0,3,1]],
                     2:[[1,2,1],[0,2,1],[1,1,1],[0,1,1],[1,3,1],[0,3,1]],
                     3:[[1,2,2],[0,2,2],[1,1,1],[0,1,1],[1,3,1],[0,3,1]]
        }
        begin_time = cls.get_day_start_unix()
        end_time = begin_time + 86400
        current_time = int(time.time())
        count = 0
        for i in range(0,6):
            up = arg_dict[3][i][0]
            stat = arg_dict[3][i][1]
            sort_type = arg_dict[3][i][2]
            cursor = cls.get_seckills(up,stat,sort_type,-1,begin_time,end_time,current_time)
            count += cursor.count()
        info_log.info('begin_time:%d end_time:%d count:%d'%(begin_time,end_time,count))
        return count
    @classmethod
    def get_seckills(cls,top_type,stat,sort_type,order,begin_time,end_time,current_time):
        '''
        stat 1表示即将开始，2表示进行中，3表示以结束
        top_type 1表示置顶，2表示非置顶
        sort_type 1表示按时间（对于即将开始，离开始时间越近越靠前；对于进行中，离结束时间越近越靠前），2表示按价格（只对进行中状态生效）
        begin_time 表示需要select结果的开始时间
        end_time 表示select结果的最后时间
        current_time 当前时间，处于即将开始状态的的开始时间大于该时间则自动进入下一个状态
        order 1表示正序，-1表示倒序
        '''
        wait_limit_time = current_time - NO_PRICE_WAIT_TIME
        if top_type == 1:
            if stat == 1:
                cursor = cls.seckills.find({'up':1,'stat':stat,'display_time_end':{"$gt":current_time,"$lt":end_time},'display_time_begin':{"$gt":current_time,"$lte":end_time}},{'_id':0}).sort('display_time_begin',order)
            elif stat == 2:
                if sort_type == 1:
                    cursor = cls.seckills.find({'up':1,'stat':stat,'display_time_end':{"$gt":current_time,"$lt":end_time},'display_time_begin':{"$gte":begin_time,"$lte":current_time},'$or':[{'cur_price':{'$gt':0}},{'display_time_begin':{'$gt':wait_limit_time}}]},{'_id':0}).sort('display_time_end',order)
                else:
                    cursor = cls.seckills.find({'up':1,'stat':stat,'display_time_end':{"$gt":current_time,"$lt":end_time},'display_time_begin':{"$gte":begin_time,"$lte":current_time},'$or':[{'cur_price':{'$gt':0}},{'display_time_begin':{'$gt':wait_limit_time}}]},{'_id':0}).sort('cur_price',order)
            else:
                cursor = cls.seckills.find({'up':1,'stat':{'$in':[1,2,stat]},'display_time_begin':{"$gte":begin_time},'display_time_end':{"$gt":begin_time,"$lt":current_time}},{'_id':0}).sort('display_time_end',order)
        else:
            if stat == 1:
                cursor = cls.seckills.find({'up':{'$ne':1},'stat':stat,'display_time_end':{"$gt":current_time,"$lt":end_time},'display_time_begin':{"$gt":current_time,"$lte":end_time}},{'_id':0}).sort('display_time_begin',order)
            elif stat == 2:
                if sort_type == 1:
                    cursor = cls.seckills.find({'up':{'$ne':1},'display_time_end':{"$gt":current_time,"$lt":end_time},'display_time_begin':{"$gte":begin_time,"$lte":current_time},'stat':{'$in':[1,stat]},'$or':[{'cur_price':{'$gt':0}},{'display_time_begin':{'$gt':wait_limit_time}}]},{'_id':0}).sort('display_time_end',order)
                else:
                    cursor = cls.seckills.find({'up':{'$ne':1},'display_time_end':{"$gt":current_time,"$lt":end_time},'display_time_begin':{"$gte":begin_time,"$lte":current_time},'stat':{'$in':[1,stat]},'$or':[{'cur_price':{'$gt':0}},{'display_time_begin':{'$gt':wait_limit_time}}]},{'_id':0}).sort('cur_price',order)
            else:
                cursor = cls.seckills.find({'up':{'$ne':1},'stat':{'$in':[1,2,stat]},'display_time_begin':{"$gte":begin_time},'display_time_end':{"$gte":begin_time,"$lt":current_time}},{'_id':0}).sort('display_time_end',order)
        return cursor
    @classmethod
    def get_seckill_link_by_id(cls,id):
       return cls.seckills.find_one({'id':id},{'id':1,'link':1})

