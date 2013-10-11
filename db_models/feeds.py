#encoding=utf8
__author__ = 'shenbin shenbin@maimiaotech.com'

from ztmhs.zhs import settings
from ztmhs.zhs.settings import TOP_RET_NUM
from ztmhs.zhs.settings import PAGE_RET_NUM

class Feeds(object):
    """
    class to operate feeds
    """
    _conn = settings.mongoConn
    _db = "scrapy"
    if _conn != None:
        feeds = _conn[_db]['ztmhs']
        links = _conn[_db]['linkdb']
    else:
        feeds = None
        links = None

    #feed_id:feed id link_id link id page:页号 num:第几位 c_type:1 标题，2 图片，3 直达链接 4 文字链接 s_type：0 全部 1白菜价 2全网最低 3 其他
    @classmethod
    def create_link_flag(cls,feed_id,link_id,page,num,c_type,s_type,t_type):
        return'fd=%s&lk=%s&pg=%d&nm=%d&ct=%d&st=%d&tt=%d'%(feed_id,link_id,page,num,c_type,s_type,t_type)

    @classmethod
    def get_all_feeds_ret_1(cls,page_num,type):
        if page_num == 1:
            top_feeds = cls.get_top_feeds(page_num,type)
        else:
            top_feeds = []
        top_n = len(top_feeds)
        com_feeds = cls.get_common_feeds(page_num,type,top_n)
        return top_feeds + com_feeds
    @classmethod
    def get_all_feeds_ret_2(cls,page_num,type):
        if page_num == 1:
            top_feeds = cls.get_top_feeds(page_num,type)
        else:
            top_feeds = []
        top_n = len(top_feeds)
        com_feeds = cls.get_common_feeds(page_num,type,top_n)
        return top_feeds,com_feeds
    @classmethod
    def get_common_feeds(cls,page_num,type,top_num=0):
        if top_num > PAGE_RET_NUM:
            top_num = PAGE_RET_NUM
        if page_num > 0:
            if page_num == 1:
                skip_num = 0
                limit_num = PAGE_RET_NUM - top_num
            else:
                skip_num = PAGE_RET_NUM * (page_num - 1) - top_num
                limit_num = PAGE_RET_NUM
            if type == 0:
                cursor = cls.feeds.find({'stat':{'$in':[1,4]},'up':2},{'_id':0}).sort('pub_time',-1).skip(skip_num).limit(limit_num)
            else:
                #1 白菜价，2 全网最低，3 其它
                cursor = cls.feeds.find({'stat':{'$in':[1,4]},'up':2,'our_cat':type},{'_id':0}).sort('pub_time',-1).skip(skip_num).limit(limit_num)
                #return [doc for doc in cursor]
        else:
            return []
        ret_list = []
        i = 0
        if page_num == 1:
            i = top_num
        for item in cursor:
            for pair in item['desc_link']:
                pair[1] = cls.create_link_flag(item['id'],pair[1],page_num,i,4,type,0)
            item['title_link_id'] = cls.create_link_flag(item['id'],item['go_link_id'],page_num,i,1,type,0)
            item['img_link_id'] = cls.create_link_flag(item['id'],item['go_link_id'],page_num,i,2,type,0)
            item['go_link_id'] = cls.create_link_flag(item['id'],item['go_link_id'],page_num,i,3,type,0)
            ret_list.append(item)
            i += 1
        return ret_list
    @classmethod
    def get_top_feeds(cls,page_num,type):
        if page_num == 0:
            return []
        if type == 0:
            cursor = cls.feeds.find({'up':1},{'_id':0}).sort('pub_time',-1).limit(TOP_RET_NUM)
        else:
            cursor = cls.feeds.find({'up':1,'our_cat':type},{'_id':0}).sort('pub_time',-1).limit(TOP_RET_NUM)
        i = 0
        ret_list = []
        for item in cursor:
            #process desc_link
            for pair in item['desc_link']:
                pair[1] = cls.create_link_flag(item['id'],pair[1],0,i,4,type,1)
            item['title_link_id'] = cls.create_link_flag(item['id'],item['go_link_id'],0,i,1,type,1)
            item['img_link_id'] = cls.create_link_flag(item['id'],item['go_link_id'],0,i,2,type,1)
            item['go_link_id'] = cls.create_link_flag(item['id'],item['go_link_id'],0,i,3,type,1)
            ret_list.append(item)
            i += 1
        return ret_list

    @classmethod
    def get_feed_url_by_linkid(cls, id):
        return cls.links.find_one({'id':id})

    @classmethod
    def add_worth(cls, id):
        cls.feeds.update({'id':id},{'$inc':{'worth':1}},multi=True)

    @classmethod
    def add_bad(cls, id):
        cls.feeds.update({'id':id},{'$inc':{'bad':1}},multi=True)

    @classmethod
    def get_feeds_count(cls, type):
        if type == 0:
            return cls.feeds.find({'stat':1}).count()
        else:
            return cls.feeds.find({'stat':1,'our_cat':type}).count()

