from rest_framework import serializers
from repository import models
from repository.models import Permission, Role


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    permission = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = '__all__'

    @staticmethod
    def get_permission(obj):
        permission_obj = obj.permission
        ser_permission = PermissionSerializer(instance=permission_obj, many=True)
        return ser_permission.data


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = models.UserProfile
        fields = '__all__'

    @staticmethod
    def get_role(obj):
        role_obj = obj.role
        ser_role = RoleSerializer(instance=role_obj)
        return ser_role.data


class BusinessUnitSerializer(serializers.ModelSerializer):
    contact = serializers.SerializerMethodField()
    manager = serializers.SerializerMethodField()

    class Meta:
        model = models.BusinessUnit
        fields = '__all__'

    @staticmethod
    def get_contact(obj):
        contact_obj = obj.contact
        ser_contact = UserProfileSerializer(instance=contact_obj)
        return ser_contact.data

    @staticmethod
    def get_manager(obj):
        manager_obj = obj.manager
        ser_manager = UserProfileSerializer(instance=manager_obj)
        return ser_manager.data


class IDCSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IDC
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):
    device_type = serializers.CharField(source='get_device_type_id_display')
    device_status = serializers.CharField(source='get_device_status_id_display')
    device_type_id = serializers.CharField(write_only=True)
    device_status_id = serializers.CharField(write_only=True)
    latest_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    idc = serializers.SerializerMethodField()
    business_unit = serializers.SerializerMethodField()

    class Meta:
        model = models.Asset
        fields = '__all__'

    @staticmethod
    def get_idc(obj):
        idc_obj = obj.idc
        ser_idc = IDCSerializer(instance=idc_obj)
        return ser_idc.data

    @staticmethod
    def get_business_unit(obj):
        bu_obj = obj.business_unit
        ser_bu = BusinessUnitSerializer(instance=bu_obj)
        return ser_bu.data


class DiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Disk
        fields = '__all__'


class NICSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NIC
        fields = '__all__'


class ServerSerializer(serializers.ModelSerializer):
    asset = serializers.SerializerMethodField()
    disk = serializers.SerializerMethodField()
    nic = serializers.SerializerMethodField()

    class Meta:
        model = models.Server
        fields = '__all__'
        # depth = 3

    @staticmethod
    def get_asset(obj):
        # print(obj, type(obj))
        asset_obj = obj.asset
        ser_asset = AssetSerializer(instance=asset_obj)
        return ser_asset.data

    @staticmethod
    def get_disk(obj):
        disk_obj_list = obj.disk.all()
        ser_disk = DiskSerializer(instance=disk_obj_list, many=True)
        return ser_disk.data

    @staticmethod
    def get_nic(obj):
        nic_obj_list = obj.nic.all()
        ser_nic = NICSerializer(instance=nic_obj_list, many=True)
        return ser_nic.data


class NetworkDeviceSerializer(serializers.ModelSerializer):
    asset = serializers.SerializerMethodField()

    class Meta:
        model = models.NetworkDevice
        fields = '__all__'

    @staticmethod
    def get_asset(obj):
        # print(obj, type(obj))
        asset_obj = obj.asset
        ser_asset = AssetSerializer(instance=asset_obj)
        return ser_asset.data


class ErrorLogSerializer(serializers.ModelSerializer):
    asset_obj = serializers.SerializerMethodField()
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.ErrorLog
        fields = '__all__'

    @staticmethod
    def get_asset_obj(obj):

        asset_obj = obj.asset_obj
        if asset_obj.device_type_id == 1:
            ser_asset = ServerSerializer(instance=asset_obj.server)
        else:
            ser_asset = NetworkDeviceSerializer(instance=asset_obj.networkdevice)
        return ser_asset.data


class AssetRecord(serializers.ModelSerializer):
    asset_obj = serializers.SerializerMethodField()
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    creator = serializers.SerializerMethodField()

    class Meta:
        model = models.AssetRecord
        fields = '__all__'

    @staticmethod
    def get_asset_obj(obj):

        asset_obj = obj.asset_obj
        if asset_obj.device_type_id == 1:
            ser_asset = ServerSerializer(instance=asset_obj.server)
        else:
            ser_asset = NetworkDeviceSerializer(instance=asset_obj.networkdevice)
        return ser_asset.data

    @staticmethod
    def get_creator(obj):
        creator_obj = obj.creator
        ser_creator = UserProfileSerializer(instance=creator_obj)
        return ser_creator.data
