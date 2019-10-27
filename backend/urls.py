from django.conf.urls import url
from backend import views
from backend.api import switch, server, firewall, load_balance, router, errlog, change_record, permission, role, \
    user_list

from backend.tests import test_get_info

from rest_framework_jwt import views as jwt_views

urlpatterns = [
    # url('^server/$', server.Server.as_view({'get': 'list', 'post': 'create'})),
    # url('^server/(?P<pk>[0-9]+)/$', views.Server.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    url('^user/login/$', views.UserLogin.as_view({'post': 'post'})),
    # url('^user/info/$', views.UserInfo.as_view({'get': 'list'})),
    url('^switch/$', switch.Switch.as_view({'get': 'list'})),
    # url('^switch/(?P<pk>[0-9]+)/$', switch.Switch.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    url('^server/$', server.Server.as_view({'get': 'list'})),
    url('^firewall/$', firewall.Firewall.as_view({'get': 'list'})),
    url('^router/$', router.Router.as_view({'get': 'list'})),
    url('^load_balance/$', load_balance.LoadBalance.as_view({'get': 'list'})),
    url('^error_log/$', errlog.ErrorLog.as_view({'get': 'list'})),
    url('^change_record/$', change_record.ChangeRecord.as_view({'get': 'list'})),
    url('^permission/$', permission.Permission.as_view({'get': 'list'})),
    url('^role/$', role.Role.as_view({'get': 'list'})),
    url('^user_list/$', user_list.UserList.as_view({'get': 'list'})),
    url('^user/info/$', test_get_info),
    # url('^user/login/$', jwt_views.obtain_jwt_token)

]
