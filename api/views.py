import hashlib
import time

from django.shortcuts import render, HttpResponse
import json
from repository import models


# from django.views import View
# from django.http.request import QueryDict


# 加密salt
key_record = {
    # "548aa8aeb09db415d168b1010016a38c" : 123123143.123
}


def entry(request):
    res = request.body
    posted_data = json.loads(res.decode(encoding='utf8'))
    hostname = posted_data['basic']['data']['hostname']
    server_obj_queryset = models.Server.objects.filter(hostname=hostname)

    if not server_obj_queryset:
        return HttpResponse('该资产尚未录入')
    server_obj = server_obj_queryset.first()
    asset_obj = server_obj.asset

    clean_basic(posted_data, server_obj_queryset, server_obj, asset_obj)
    clean_board(posted_data, server_obj_queryset, server_obj, asset_obj)
    clean_cpu(posted_data, server_obj_queryset, server_obj, asset_obj)
    clean_disk(posted_data, server_obj, asset_obj)
    clean_memory(posted_data, server_obj, asset_obj)
    clean_nic(posted_data, server_obj, asset_obj)
    asset_obj.save()
    return HttpResponse('successful')


def asset(request):
    if request.method == 'GET':
        server_token = "vdgsavhdsbhafbsdbfhbdshfbsd"
        server_time = time.time()
        client_md5_header = request.META.get('HTTP_TOKEN')
        if client_md5_header == None:
            return HttpResponse('没有权限')
        client_md5_token, client_time = client_md5_header.split('|')
        client_time = float(client_time)

        if server_time - client_time > 10:
            return HttpResponse('[第一关] 小伙子, 时间太久了.....')

        tmp = "%s|%s" % (server_token, client_time)
        m = hashlib.md5()
        m.update(bytes(tmp, encoding='utf-8'))
        server_md5_token = m.hexdigest()

        if server_md5_token != client_md5_token:
            return HttpResponse('[第二关] 你是不是修改了token')

        for k in list(key_record.keys()):
            if server_time > key_record[k]:
                del key_record[k]

        if client_md5_token in key_record:
            return HttpResponse('[第三关] 已经被别人访问过了')
        else:
            key_record[client_md5_token] = client_time + 10

        return HttpResponse('ok')

    elif request.method == 'POST':
        res = request.body
        new_server_info = json.loads(res)
        # print(new_server_info)

        hostname = new_server_info['basic']['data']['hostname']

        old_server_obj = models.Server.objects.filter(hostname=hostname).first()
        # print(old_server_obj)

        if not old_server_obj:
            return HttpResponse('该资产并未录入...')

        # 开始清理  disk  memory  nic  board
        if new_server_info['disk']['status'] != 10000:
            models.ErrorLog.objects.create(asset_obj=old_server_obj, title="(%s)的硬盘采集出错了" % hostname,
                                           content=new_server_info['disk']['data'])

        # memory {'DIMM #0': {'capacity': 1024, 'slot': 'DIMM #0', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'DIMM #1': {'capacity': 0, 'slot': 'DIMM #1', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'DIMM #2': {'capacity': 0, 'slot': 'DIMM #2', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'DIMM #3': {'capacity': 0, 'slot': 'DIMM #3', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'DIMM #4': {'capacity': 0, 'slot': 'DIMM #4', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'DIMM #5': {'capacity': 0, 'slot': 'DIMM #5', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'DIMM #6': {'capacity': 0, 'slot': 'DIMM #6', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'DIMM #7': {'capacity': 0, 'slot': 'DIMM #7', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}}}
        # old [4,5,6]
        # new [4,5,7]
        '''
        new_disk_info
           '0': 
               {'slot': '0', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}, 
           '1': 
               {'slot': '1', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5AH'}, 
           '2': 
               {'slot': '2', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1SZNSAFA01085L     Samsung SSD 850 PRO 512GB               EXM01B6Q'}, 
        '''
        '''
        old_disk_info
           [
               Disk(slot=0, model),
               Disk(slot=1, model),
           ]
        '''
        old_disk_info = models.Disk.objects.filter(server_obj=old_server_obj)
        new_disk_info = new_server_info['disk']['data']

        # print(new_disk_info)

        # [0,1,2,3,4,5]
        new_slot_list = list(new_disk_info.keys())
        old_slot_list = []
        for v in old_disk_info:
            old_slot_list.append(v.slot)

        '''
         new_slot_list: [1,2,3]
         old_slot_list: [1,2,4]
        '''
        # 1.增加的slot
        add_slot_list = set(new_slot_list).difference(set(old_slot_list))
        print(add_slot_list)

        if add_slot_list:
            # disk_res = {}
            recoder_list = []
            for v in add_slot_list:
                # {'slot': '0', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}
                disk_res = new_disk_info[v]
                tmp = "增加磁盘槽位{slot}, 类型{pd_type}, 容量{capacity}, 型号{model}".format(**disk_res)
                disk_res['server_obj'] = old_server_obj
                models.Disk.objects.create(**disk_res)
                recoder_list.append(tmp)

            recoder_str = ";".join(recoder_list)
            models.AssetRecord.objects.create(asset_obj=old_server_obj, content=recoder_str)

        # 2. 删除的slot
        del_slot_list = set(old_slot_list).difference(set(new_slot_list))
        print(del_slot_list)
        # delete from disk where slot in (2,3,4)
        if del_slot_list:
            # for slot in del_slot_list:
            models.Disk.objects.filter(slot__in=del_slot_list, server_obj=old_server_obj).delete()

            del_str = "删除的槽位是%s" % (";".join(del_slot_list))
            models.AssetRecord.objects.create(asset_obj=old_server_obj, content=del_str)

        # 3. 更新的slot
        up_slot_list = set(old_slot_list).intersection(set(new_slot_list))
        print(up_slot_list)

        if up_slot_list:
            recoder_list = []
            for slot in up_slot_list:
                old_disk_row = models.Disk.objects.filter(slot=slot, server_obj=old_server_obj).first()  # [disk(slot)]
                # {'slot': '0', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}
                new_disk_row = new_disk_info[slot]
                for k, new_v in new_disk_row.items():
                    '''
                    k: slot, pd_type, model
                    new_v: SAS
                    '''
                    old_v = getattr(old_disk_row, k)
                    if old_v != new_v:
                        tmp = "槽位:%s, %s由%s更改为%s" % (slot, k, old_v, new_v)
                        recoder_list.append(tmp)
                        setattr(old_disk_row, k, new_v)
                old_disk_row.save()

            if recoder_list:
                models.AssetRecord.objects.create(asset_obj=old_server_obj, content=";".join(recoder_list))

    return HttpResponse('ok')


def clean_basic(posted_data, server_obj_queryset, server_obj, asset_obj):
    basic_data = posted_data['basic']
    if basic_data['status_code'] != 10000:
        error_title = basic_data['data']['title']
        error_content = basic_data['data']['content']
        models.ErrorLog.objects.create(asset_obj=asset_obj, title=error_title, content=error_content)
    else:
        update_info = {}
        update_content = ''
        for k, new_v in basic_data['data'].items():
            old_v = getattr(server_obj, k)
            if old_v != new_v:
                update_info[k] = new_v
                update_content += '信息【%s】:【%s】已变为【%s】; ' % ('basic', k, new_v)
        if update_info:
            server_obj_queryset.update(**update_info)
            models.AssetRecord.objects.create(asset_obj=asset_obj, content=update_content)


def clean_cpu(posted_data, server_obj_queryset, server_obj, asset_obj):
    cpu_data = posted_data['cpu']
    if cpu_data['status_code'] != 10000:
        error_title = cpu_data['data']['title']
        error_content = cpu_data['data']['content']
        models.ErrorLog.objects.create(asset_obj=asset_obj, title=error_title, content=error_content)
    else:
        update_info = {}
        update_content = ''

        for k, new_v in cpu_data['data'].items():
            old_v = getattr(server_obj, k)
            if old_v != new_v:
                update_info[k] = new_v
                update_info[k] = new_v
                update_content += '信息【%s】:【%s】已变为【%s】; ' % ('cpu', k, new_v)
        if update_info:
            server_obj_queryset.update(**update_info)
            models.AssetRecord.objects.create(asset_obj=asset_obj, content=update_content)


def clean_board(posted_data, server_obj_queryset, server_obj, asset_obj):
    board_data = posted_data['board']
    if board_data['status_code'] != 10000:
        error_title = board_data['data']['title']
        error_content = board_data['data']['content']
        models.ErrorLog.objects.create(asset_obj=asset_obj, title=error_title, content=error_content)

    else:
        update_info = {}
        update_content = ''
        for k, new_v in board_data['data'].items():
            old_v = getattr(server_obj, k)
            if old_v != new_v:
                update_info[k] = new_v
                update_info[k] = new_v
                update_content += '信息【%s】:【%s】已变为【%s】; ' % ('board', k, new_v)
        if update_info:
            server_obj_queryset.update(**update_info)
            models.AssetRecord.objects.create(asset_obj=asset_obj, content=update_content)


def clean_disk(posted_data, server_obj, asset_obj):
    disk_data = posted_data['disk']
    if disk_data['status_code'] != 10000:
        error_title = disk_data['data']['title']
        error_content = disk_data['data']['content']
        models.ErrorLog.objects.create(asset_obj=asset_obj, title=error_title, content=error_content)
    else:
        new_disk_slot_list = list(disk_data['data'].keys())
        old_disk_slot_list = []
        old_disk_obj_list = models.Disk.objects.filter(server_obj=server_obj).all()

        for disk_obj in old_disk_obj_list:
            old_disk_slot_list.append(disk_obj.slot)

        add_disk_slot = set(new_disk_slot_list) - set(old_disk_slot_list)
        if add_disk_slot:

            for disk_slot_info in add_disk_slot:
                disk_info = disk_data['data'][disk_slot_info]
                disk_info['server_obj_id'] = server_obj.id
                models.Disk.objects.create(**disk_info)
                update_content = '服务器%s的%s槽位增加一块磁盘：%s' % (server_obj.hostname, disk_slot_info, disk_info)
                models.AssetRecord.objects.create(asset_obj=asset_obj, content=update_content)

        delete_disk_slot = set(old_disk_slot_list) - set(new_disk_slot_list)
        if delete_disk_slot:
            for disk_slot_info in delete_disk_slot:
                disk_obj = models.Disk.objects.filter(slot=disk_slot_info, server_obj=server_obj).first()
                disk_info = {
                    'server_obj_id': getattr(disk_obj, 'server_obj_id'),
                    'slot': getattr(disk_obj, 'slot'),
                    'model': getattr(disk_obj, 'model'),
                    'capacity': getattr(disk_obj, 'capacity'),
                    'pd_type': getattr(disk_obj, 'pd_type')
                }
                models.Disk.objects.filter(slot=disk_slot_info, server_obj=server_obj).delete()
                update_content = '服务器%s的槽位%s移除一块磁盘：%s' % (server_obj.hostname, disk_slot_info, disk_info)
                models.AssetRecord.objects.create(asset_obj=asset_obj, content=update_content)

        update_disk_slot = set(old_disk_slot_list) & set(new_disk_slot_list)
        if update_disk_slot:
            for disk_slot_info in update_disk_slot:
                disk_obj = models.Disk.objects.filter(slot=disk_slot_info, server_obj=server_obj).first()
                old_disk_info = {
                    'server_obj_id': getattr(disk_obj, 'server_obj_id'),
                    'slot': getattr(disk_obj, 'slot'),
                    'model': getattr(disk_obj, 'model'),
                    'capacity': getattr(disk_obj, 'capacity'),
                    'pd_type': getattr(disk_obj, 'pd_type')
                }
                new_disk_info = disk_data['data'][disk_slot_info]
                new_disk_info['server_obj_id'] = server_obj.id

                if old_disk_info != new_disk_info:
                    new_disk_info['server_obj_id'] = server_obj.id
                    models.Disk.objects.filter(slot=disk_slot_info, server_obj=server_obj).update(**new_disk_info)

                    update_content = '服务器%s槽位%s的磁盘从%s变更为%s' % (server_obj.hostname, disk_slot_info,
                                                               old_disk_info, new_disk_info)
                    models.AssetRecord.objects.create(asset_obj=asset_obj, content=update_content)


def clean_memory(posted_data, server_obj, asset_obj):
    memory_data = posted_data['memory']
    if memory_data['status_code'] != 10000:
        error_title = memory_data['data']['title']
        error_content = memory_data['data']['content']
        models.ErrorLog.objects.create(asset_obj=asset_obj, title=error_title, content=error_content)
    else:
        new_memory_slot_list = list(memory_data['data'].keys())
        old_memory_slot_list = []
        old_memory_obj_list = models.Memory.objects.filter(server_obj=server_obj).all()

        for memory_obj in old_memory_obj_list:
            old_memory_slot_list.append(memory_obj.slot)

        add_memory_slot = set(new_memory_slot_list) - set(old_memory_slot_list)
        if add_memory_slot:

            for memory_slot_info in add_memory_slot:
                memory_info = memory_data['data'][memory_slot_info]
                memory_info['server_obj_id'] = server_obj.id
                models.Memory.objects.create(**memory_info)
                update_content = '服务器%s的%s槽位增加一条内存：%s' % (server_obj.hostname, memory_slot_info, memory_info)
                models.AssetRecord.objects.create(asset_obj=asset_obj, content=update_content)

        delete_memory_slot = set(old_memory_slot_list) - set(new_memory_slot_list)
        if delete_memory_slot:
            for memory_slot_info in delete_memory_slot:
                memory_obj = models.Memory.objects.filter(slot=memory_slot_info, server_obj=server_obj).first()
                memory_info = {
                    'server_obj_id': getattr(memory_obj, 'server_obj_id'),
                    'slot': getattr(memory_obj, 'slot'),
                    'manufacturer': getattr(memory_obj, 'manufacturer'),
                    'speed': getattr(memory_obj, 'speed'),
                    'capacity': getattr(memory_obj, 'capacity'),
                    'model': getattr(memory_obj, 'model'),
                    'sn': getattr(memory_obj, 'sn'),
                }
                models.Memory.objects.filter(slot=memory_slot_info, server_obj=server_obj).delete()
                update_content = '服务器%s的槽位%s移除一条内存：%s' % (server_obj.hostname, memory_slot_info, memory_info)
                models.AssetRecord.objects.create(asset_obj=asset_obj, content=update_content)

        update_memory_slot = set(old_memory_slot_list) & set(new_memory_slot_list)
        if update_memory_slot:
            for memory_slot_info in update_memory_slot:
                memory_obj = models.Memory.objects.filter(slot=memory_slot_info, server_obj=server_obj).first()
                old_memory_info = {
                    'server_obj_id': getattr(memory_obj, 'server_obj_id'),
                    'slot': getattr(memory_obj, 'slot'),
                    'manufacturer': getattr(memory_obj, 'manufacturer'),
                    'speed': getattr(memory_obj, 'speed'),
                    'capacity': getattr(memory_obj, 'capacity'),
                    'model': getattr(memory_obj, 'model'),
                    'sn': getattr(memory_obj, 'sn'),
                }
                new_memory_info = memory_data['data'][memory_slot_info]
                new_memory_info['server_obj_id'] = server_obj.id
                if old_memory_info != new_memory_info:
                    new_memory_info['server_obj_id'] = server_obj.id
                    models.Memory.objects.filter(slot=memory_slot_info, server_obj=server_obj).update(**new_memory_info)

                    update_content = '服务器%s槽位%s的内存从%s变更为%s' % (server_obj.hostname, memory_slot_info,
                                                               old_memory_info, new_memory_info)
                    models.AssetRecord.objects.create(asset_obj=asset_obj, content=update_content)


def clean_nic(posted_data, server_obj, asset_obj):
    nic_data = posted_data['nic']
    if nic_data['status_code'] != 10000:
        error_title = nic_data['data']['title']
        error_content = nic_data['data']['content']
        models.ErrorLog.objects.create(asset_obj=asset_obj, title=error_title, content=error_content)
    else:
        new_nic_name_list = list(nic_data['data'].keys())
        old_nic_name_list = []
        old_nic_obj_list = models.NIC.objects.filter(server_obj=server_obj).all()

        for nic_obj in old_nic_obj_list:
            old_nic_name_list.append(nic_obj.name)

        add_nic_name = set(new_nic_name_list) - set(old_nic_name_list)
        if add_nic_name:

            for nic_name in add_nic_name:
                nic_info = nic_data['data'][nic_name]
                nic_info['server_obj_id'] = server_obj.id
                nic_info['name'] = nic_name
                models.NIC.objects.create(**nic_info)
                update_content = '服务器%s增加一块网卡%s：%s' % (server_obj.hostname, nic_name, nic_info)
                models.AssetRecord.objects.create(asset_obj=asset_obj, content=update_content)

        delete_nic_name = set(old_nic_name_list) - set(new_nic_name_list)
        if delete_nic_name:
            for nic_name in delete_nic_name:
                nic_obj = models.NIC.objects.filter(name=nic_name, server_obj=server_obj).first()
                nic_info = {
                    'server_obj_id': getattr(nic_obj, 'server_obj_id'),
                    'name': getattr(nic_obj, 'name'),
                    'hwaddr': getattr(nic_obj, 'hwaddr'),
                    'netmask': getattr(nic_obj, 'netmask'),
                    'ipaddrs': getattr(nic_obj, 'ipaddrs'),
                    'up': getattr(nic_obj, 'up'),

                }
                models.NIC.objects.filter(name=nic_name, server_obj=server_obj).delete()
                update_content = '服务器%s移除一块网卡%s：%s' % (server_obj.hostname, nic_name, nic_info)
                models.AssetRecord.objects.create(asset_obj=asset_obj, content=update_content)

        update_nic_name = set(old_nic_name_list) & set(new_nic_name_list)
        if update_nic_name:
            for nic_name in update_nic_name:
                nic_obj = models.NIC.objects.filter(name=nic_name, server_obj=server_obj).first()
                old_nic_info = {
                    'server_obj_id': getattr(nic_obj, 'server_obj_id'),
                    'name': getattr(nic_obj, 'name'),
                    'hwaddr': getattr(nic_obj, 'hwaddr'),
                    'netmask': getattr(nic_obj, 'netmask'),
                    'ipaddrs': getattr(nic_obj, 'ipaddrs'),
                    'up': getattr(nic_obj, 'up'),
                }
                new_nic_info = nic_data['data'][nic_name]
                new_nic_info['server_obj_id'] = server_obj.id
                new_nic_info['name'] = nic_name

                if new_nic_info != old_nic_info:
                    new_nic_info['server_obj_id'] = server_obj.id
                    models.NIC.objects.filter(name=nic_name, server_obj=server_obj).update(**new_nic_info)

                    update_content = '服务器%s网卡%s信息由%s变更为%s' % (server_obj.hostname, nic_name,
                                                              old_nic_info, new_nic_info)
                    models.AssetRecord.objects.create(asset_obj=asset_obj, content=update_content)
