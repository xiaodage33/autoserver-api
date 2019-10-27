from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(models.Model):
    """
    用户信息
    """
    name = models.CharField(max_length=64, verbose_name=u'姓名')
    email = models.EmailField(verbose_name=u'邮箱')
    phone = models.CharField(max_length=64, verbose_name=u'座机')
    mobile = models.CharField(max_length=64, verbose_name=u'手机')
    username = models.CharField(max_length=64, verbose_name=u'用户名', unique=True)
    password = models.CharField(max_length=64, verbose_name=u'密码')
    role = models.ForeignKey(to='Role', verbose_name=u'角色')

    class Meta:
        verbose_name_plural = u'用户表'

    def __str__(self):
        return self.name


class Role(models.Model):
    """
    角色信息，用于区分权限
    """
    name = models.CharField(max_length=64, verbose_name=u'角色名', unique=True)
    chinese_name = models.CharField(max_length=128, verbose_name=u'中文角色名', unique=True)
    permission = models.ManyToManyField(to='Permission', verbose_name=u'权限')

    class Meta:
        verbose_name_plural = u'角色表'

    def __str__(self):
        return self.name


class Permission(models.Model):
    """
    权限信息，用于区分权限
    """
    name = models.CharField(max_length=64, verbose_name=u'权限名称', unique=True)
    chinese_name = models.CharField(max_length=128, verbose_name=u'中文权限名', unique=True)

    class Meta:
        verbose_name_plural = u'用户权限表'

    def __str__(self):
        return self.name


'''
class UserGroup(models.Model):
    """
    用户组信息
    """
    name = models.CharField(max_length=64, verbose_name=u'组名', unique=True)
    user = models.ManyToManyField(to='UserProfile', through_fields=('group', 'user'), through='UserProfile2UserGroup')

    class Meta:
        verbose_name_plural = u'用户组表'

    def __str__(self):
        return self.name


class UserProfile2UserGroup(models.Model):
    """
    用户与用户组多对多映射表
    """
    user = models.ForeignKey(to='UserProfile')
    group = models.ForeignKey(to='UserGroup')

    class Meta:
        verbose_name_plural = u'用户与用户组多对多映射表'
'''


class BusinessUnit(models.Model):
    """
    业务线表
    """
    name = models.CharField(max_length=64, verbose_name=u'业务名称', unique=True)
    contact = models.ForeignKey(to='UserProfile', verbose_name=u'业务联系人', related_name='c')
    manager = models.ForeignKey(to='UserProfile', verbose_name=u'业务负责人', related_name='m')

    class Meta:
        verbose_name_plural = u'业务线表'

    def __str__(self):
        return self.name


class IDC(models.Model):
    """
    机房信息
    """
    name = models.CharField(max_length=64, verbose_name=u'机房名称', unique=True)

    class Meta:
        verbose_name_plural = u'机房表'

    def __str__(self):
        return self.name


'''
class Tag(models.Model):
    """
    资产标签
    """
    name = models.CharField(max_length=64, verbose_name=u'标签', unique=True)

    class Meta:
        verbose_name_plural = u'资产标签表'

    def __str__(self):
        return self.name
'''


class Asset(models.Model):
    """
    资产表
    """
    device_type = (
        (1, u'服务器'),
        (2, u'交换机'),
        (3, u'路由器'),
        (4, u'防火墙'),
        (5, u'负载均衡器')
    )
    device_status = (
        (1, u'上架'),
        (2, u'离线'),
        (3, u'在线'),
        (4, u'下架')
    )

    device_type_id = models.IntegerField(choices=device_type, default=1)
    device_status_id = models.IntegerField(choices=device_status, default=1)

    cabinet_num = models.CharField(verbose_name=u'机柜号', max_length=32, null=True, blank=True)
    cabinet_order = models.CharField(verbose_name=u'机柜中序号', max_length=32, null=True, blank=True)

    idc = models.ForeignKey(to='IDC', verbose_name='机房', null=True, blank=True)
    business_unit = models.ForeignKey(to='BusinessUnit', verbose_name='业务线', null=True, blank=True)

    # tag = models.ManyToManyField(to='Tag')

    latest_date = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = u'资产表'

    def __str__(self):
        return '%s-%s-%s' % (self.idc.name, self.cabinet_num, self.cabinet_order)


class NetworkDevice(models.Model):
    """网络设备表"""
    asset = models.OneToOneField(to='Asset')
    name = models.CharField(verbose_name='设备名称', max_length=64, blank=True, null=True)
    management_ip = models.CharField(verbose_name='管理ip', max_length=64, blank=True, null=True)
    vlan_ip = models.CharField('VlanIP', max_length=64, blank=True, null=True)
    intranet_ip = models.CharField('内网IP', max_length=128, blank=True, null=True)
    sn = models.CharField('SN号', max_length=64, unique=True)
    manufacturer = models.CharField(verbose_name=u'制造商', max_length=128, null=True, blank=True)
    model = models.CharField('型号', max_length=128, null=True, blank=True)
    port_num = models.SmallIntegerField('端口个数', null=True, blank=True)
    device_detail = models.CharField('设置详细配置', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "网络设备"


class Server(models.Model):
    """
    服务器信息
    """
    asset = models.OneToOneField(to='Asset')

    hostname = models.CharField(verbose_name=u'主机名', max_length=64, unique=True)
    sn = models.CharField(verbose_name=u"SN号", max_length=64, db_index=True, null=True, blank=True)
    manufacturer = models.CharField(verbose_name=u'制造商', max_length=64, null=True, blank=True)
    model = models.CharField(verbose_name=u'型号', max_length=64, null=True, blank=True)

    management_ip = models.GenericIPAddressField(verbose_name='管理ip', null=True, blank=True)
    os_platform = models.CharField('系统', max_length=64, null=True, blank=True)
    os_version = models.CharField('系统版本', max_length=64, null=True, blank=True)

    cpu_count = models.IntegerField('CPU个数', null=True, blank=True)
    cpu_physical_count = models.IntegerField('CPU物理个数', null=True, blank=True)
    cpu_model = models.CharField('CPU型号', max_length=128, null=True, blank=True)

    class Meta:
        verbose_name_plural = "服务器表"

    def __str__(self):
        return self.hostname


class Disk(models.Model):
    """
    硬盘信息
    """
    slot = models.CharField('插槽位', max_length=8)
    model = models.CharField('磁盘型号', max_length=128)
    capacity = models.CharField('磁盘容量GB', max_length=64)
    pd_type = models.CharField('磁盘类型', max_length=64)
    server_obj = models.ForeignKey('Server', related_name='disk')

    class Meta:
        verbose_name_plural = "硬盘表"

    def __str__(self):
        return '插槽位:%s' % self.slot


class NIC(models.Model):
    """
    网卡信息
    """
    name = models.CharField('网卡名称', max_length=128)
    hwaddr = models.CharField('网卡mac地址', max_length=64)
    netmask = models.CharField(max_length=64)
    ipaddrs = models.CharField('ip地址', max_length=256)
    up = models.BooleanField(default=False)
    server_obj = models.ForeignKey('Server', related_name='nic')

    class Meta:
        verbose_name_plural = "网卡表"

    def __str__(self):
        return self.name


class Memory(models.Model):
    """
    内存信息
    """
    slot = models.CharField('插槽位', max_length=32)
    manufacturer = models.CharField('制造商', max_length=32, null=True, blank=True)
    model = models.CharField('型号', max_length=64)
    capacity = models.FloatField('容量', null=True, blank=True)
    sn = models.CharField('内存SN号', max_length=64, null=True, blank=True)
    speed = models.CharField('速度', max_length=16, null=True, blank=True)

    server_obj = models.ForeignKey('Server', related_name='memory')

    class Meta:
        verbose_name_plural = "内存表"

    def __str__(self):
        return '插槽位:%s' % self.slot


class AssetRecord(models.Model):
    """
    资产变更记录,creator为空时，表示是资产汇报的数据。
    """
    asset_obj = models.ForeignKey('Asset', related_name='ar')
    content = models.TextField(null=True)  # 新增硬盘
    creator = models.ForeignKey('UserProfile', null=True, blank=True)  #
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "资产变更记录表"

    def __str__(self):
        return "%s-%s-%s" % (self.asset_obj.idc.name, self.asset_obj.cabinet_num, self.asset_obj.cabinet_order)


class ErrorLog(models.Model):
    """
    错误日志,如：agent采集数据错误 或 运行错误
    """
    asset_obj = models.ForeignKey('Asset', null=True, blank=True)
    title = models.CharField(max_length=64)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "错误日志表"

    def __str__(self):
        return self.title
