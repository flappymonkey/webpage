from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

handler404 = 'zhs.views.my_404_view'
handler500 = 'zhs.views.my_500_view'

urlpatterns = patterns('',
    url(r'^$', 'zhs.views.home', name='home'),
    url(r'^redirect/', 'zhs.views.redirect', name='redirect'),
    url(r'^auth/login/$', 'zhs.views.login', name='login'),
    url(r'^auth/logout/$', 'zhs.views.logout', name='logout'),
    url(r'^seckill/$', 'zhs.views.seckill', name='seckill'),
    url(r'^goldmall/$', 'zhs.views.goldmall', name='goldmall'),
)

urlpatterns += patterns('',
    url(r'^ajax_add_worth', 'zhs.ajax_views.ajax_add_worth', name='ajax_add_worth'),
    url(r'^ajax_add_bad', 'zhs.ajax_views.ajax_add_bad', name='ajax_add_bad'),
    url(r'^ajax_get_feeds', 'zhs.ajax_views.ajax_get_feeds', name='ajax_get_feeds'),
    url(r'^get_feeds_count', 'zhs.ajax_views.get_feeds_count', name='get_feeds_count'),
    url(r'^ajax_get_seckills', 'zhs.ajax_views.ajax_get_seckills', name='ajax_get_seckills'),
    url(r'^get_seckills_count', 'zhs.ajax_views.get_seckills_count', name='get_seckills_count'),
)
