from rest_framework import serializers
from repository import models
from rest_framework.response import Response

# class DiskSerializer(serializers.Serializer):
#     capacity = serializers.CharField()
#
#
# class ServerSerializer(serializers.Serializer):
#     hostname = serializers.CharField()
#     sn_num = serializers.CharField(source='sn')
#
#     asset = serializers.CharField(source='asset.get_device_type_id_display')
#     asset = serializers.SerializerMethodField()
#
#     @staticmethod
#     def get_asset(obj):
#         print(obj, type(obj))
#         # return {'sn': obj.sn, 'asset_type': obj.asset.get_device_type_id_display()}
#         disk_obj = models.Disk.objects.filter(server_obj=obj)
#         ser_disk = DiskSerializer(instance=disk_obj, many=True)
#         return ser_disk.data
#
#     def create(self, validated_data):
#         print('asdfasdfasd\n', validated_data)
#         validated_data['asset_id'] = 3
#         res = models.Server.objects.create(**validated_data)
#         return res

# class AssetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Asset
#         fields = ('hostname','sn')
#         exclude = ('hostname','sn')
#         depth = 1
#         fields = '__all__'

import datetime


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.UserProfile
        fields = '__all__'


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
