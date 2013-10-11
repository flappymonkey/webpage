#encoding=utf8
import json
from ztmhs.zhs import settings

class QQUsereInfo(object):
    @classmethod
    def get_user_info(cls,api):
        return api.request_api('user/get_user_info')

    @classmethod
    def get_weibo_info(cls,api):
        return api.request_api('user/get_info')


