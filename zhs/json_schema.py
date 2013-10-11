#! /usr/bin/env python
#! coding: utf-8
# author = shenbin
# date = 13-9-10

__int_schema = {'type': 'integer'}

__string_schema = {'type': 'string'}

__number_schema = {'type': 'number'}

__int_list_schema = {'type': 'array',
                     'items':
                             {'type': 'integer'}
}
__string_list_schema = {'type': 'array',
                     'items':
                             {'type': 'string'}
}

__number_list_schema = {'type': 'array',
                     'items':{'type': 'number'}
}

ajax_add_worth_schema = {
    'type':'object',
    'properties':{
        'id':__string_schema
    }
}

ajax_add_bad_schema = {
    'type':'object',
    'properties':{
        'id':__string_schema
    }
}

ajax_get_feeds_schema = {
    'type':'object',
    'properties':{
        'page_num':__int_schema,
        'search_type':__int_schema
    }
}

get_feeds_count_schema = {
    'type':'object',
    'properties':{
        'search_type':__int_schema
    }
}
ajax_get_seckills_schema = {
    'type':'object',
    'properties':{
        'req_type':__int_schema,
        'order':__int_schema,
        'page_num':__int_schema
    }
}

get_seckills_count_schema = {
    'type':'object',
}