from django.test import TestCase
import os
import sys


def initial():
    lll = ['雷雳军', '马小云', '周树人', '鲁宾讯', '牛榴弹', '锐雯雯', '草丛伦', '江洪潮']
    Permission.objects.create(name='edit_host', chinese_name='主机编辑')
    Permission.objects.create(name='host_transfer', chinese_name='主机转移')
    Permission.objects.create(name='edit_topology', chinese_name='拓扑编辑')
    Permission.objects.create(name='process_manage', chinese_name='进程管理')
    Permission.objects.create(name='dynamic_grouping', chinese_name='动态分组')

    per_obj = Permission.objects.all()

    Role.objects.create(name='admin', chinese_name='管理员').permission.add(*per_obj)
    Role.objects.create(name='ops', chinese_name='运维人员')
    Role.objects.create(name='developer', chinese_name='开发人员')
    Role.objects.create(name='tester', chinese_name='测试人员')
    Role.objects.create(name='operator', chinese_name='操作人员')
    Role.objects.create(name='product', chinese_name='产品人员')

    UserProfile.objects.create(name='江洪潮', email='123@qq.com', phone='119', mobile='110', username='admin',
                               password='123456', role_id=1)
    UserProfile.objects.create(name='闻琦', email='123@qq.com', phone='119', mobile='110', username='wenqi',
                               password='123456', role_id=2)
    UserProfile.objects.create(name='张昊', email='123@qq.com', phone='119', mobile='110', username='zhanghao',
                               password='123456', role_id=3)
    user_list = []
    for i in range(50):
        user_obj = UserProfile(name='%s%s' % (random.choice(lll), i), email='123@qq.com', phone='119', mobile='110',
                               username='jhc%s' % i,
                               password='123456', role_id=random.randint(1, 6))
        user_list.append(user_obj)
    UserProfile.objects.bulk_create(user_list)

    BusinessUnit.objects.create(name='网络部', contact_id=1, manager_id=1)
    BusinessUnit.objects.create(name='CTBOSS', contact_id=2, manager_id=1)
    BusinessUnit.objects.create(name='集中化经分', contact_id=3, manager_id=2)
    BusinessUnit.objects.create(name='信安中心', contact_id=1, manager_id=3)
    BusinessUnit.objects.create(name='云管平台', contact_id=random.randint(4, 50), manager_id=random.randint(4, 50))
    BusinessUnit.objects.create(name='网状网', contact_id=random.randint(4, 50), manager_id=random.randint(4, 50))
    BusinessUnit.objects.create(name='基础平台部', contact_id=random.randint(4, 50), manager_id=random.randint(4, 50))
    BusinessUnit.objects.create(name='财务集中化', contact_id=random.randint(4, 50), manager_id=random.randint(4, 50))
    BusinessUnit.objects.create(name='安全管理中心', contact_id=random.randint(4, 50), manager_id=random.randint(4, 50))
    BusinessUnit.objects.create(name='和零售', contact_id=random.randint(4, 50), manager_id=random.randint(4, 50))

    IDC.objects.create(name='哈尔滨')
    IDC.objects.create(name='呼和浩特')

    for i in range(1,51):
        asset_obj = Asset(device_status_id=random.randint(2, 3), device_type_id=2, idc_id=2, business_unit_id=1)
        asset_obj.save()
        net_obj = NetworkDevice(asset=asset_obj, name='HHHT-PCRP1-P-5960-%s' % i, management_ip='192.168.8.%s' % i,
                                vlan_ip='192.168.9.%s' % i, intranet_ip='192.168.10.%s' % i, sn='1234%s' % i,
                                manufacturer='中兴',
                                port_num=100)
        net_obj.save()
    for i in range(1,5):
        asset_obj = Asset(device_status_id=3, device_type_id=3, idc_id=2, business_unit_id=1)
        asset_obj.save()
        net_obj = NetworkDevice(asset=asset_obj, name='HHHT-PCRP1-CMNET-NE40E-%s' % i, management_ip='192.168.8.%s' % i,
                                vlan_ip='192.168.9.%s' % i, intranet_ip='192.168.10.%s' % i, sn='1d234%s' % i,
                                manufacturer='华为',
                                port_num=100)
        net_obj.save()
    for i in range(1,5):
        asset_obj = Asset(device_status_id=3, device_type_id=4, idc_id=2, business_unit_id=1)
        asset_obj.save()
        net_obj = NetworkDevice(asset=asset_obj, name='HHHT-PCRP1-CIN-E8000-%s' % i, management_ip='192.168.8.%s' % i,
                                vlan_ip='192.168.9.%s' % i, intranet_ip='192.168.10.%s' % i, sn='12dd34%s' % i,
                                manufacturer=r'山石',
                                port_num=100)
        net_obj.save()
    for i in range(1,9):
        asset_obj = Asset(device_status_id=3, device_type_id=5, idc_id=2, business_unit_id=1)
        asset_obj.save()
        net_obj = NetworkDevice(asset=asset_obj, name='HHHT-PCRP1-C-7440-%s' % i, management_ip='192.168.8.%s' % i,
                                vlan_ip='192.168.9.%s' % i, intranet_ip='192.168.10.%s' % i, sn='12dfs34%s' % i,
                                manufacturer='A10',
                                port_num=100)
        net_obj.save()
    for i in range(1,201):
        asset_obj = Asset(device_status_id=random.randint(1, 4), device_type_id=1, idc_id=2, business_unit_id=random.randint(1, 10))
        asset_obj.save()
        net_obj = Server(asset=asset_obj, hostname='HHHT-PCRP1-M-BCEC-CTL%s' % i, management_ip='192.168.8.%s' % i,
                         manufacturer='华为')
        net_obj.save()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoserver.settings")
    import django

    django.setup()
    import random
    from repository.models import *
    from django.contrib.auth import models
    initial()
