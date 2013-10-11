__author__ = 'gaonan'

from ztmhs.zhs import settings

class UserInfo(object):
    _conn = settings.mongoConn
    _db = "scrapy"
    if _conn != None:
        user_info = _conn[_db]['userinfo']
    else:
        user_info = None

    @classmethod
    def get_user_info_by_openid(cls,openid):
        if cls.user_info:
            cursor = cls.user_info.find_one({'openid':openid})
            return cursor
        else:
            return None
    @classmethod
    def save_user_info_by_openid(cls,openid,info):
        if cls.user_info:
            cls.user_info.update({'openid':openid},{'$set':{'info':dict(info)}},upsert=True, safe=True)
    @classmethod
    def save_user_weibo_info_by_openid(cls,openid,info):
        if cls.user_info:
            cls.user_info.update({'openid':openid},{'$set':{'weibo_info':dict(info)}},upsert=True, safe=True)

