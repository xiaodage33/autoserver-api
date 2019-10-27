from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView

from backend.utils.page import Page
from repository import models
from backend.cmdbSerializers.common_serializers import NetworkDeviceSerializer


class Firewall(ViewSetMixin, APIView):
    queryset = models.NetworkDevice.objects.filter(asset__device_type_id=4).order_by('-asset__latest_date')
    serializer_class = NetworkDeviceSerializer

    def list(self, request, *args, **kwargs):
        response = {'code': 20000, 'msg': None, 'data': None}
        device_name = request.query_params.get('name')
        # device_status_id = int(request.query_params.get('device_status_id'))
        page = Page()
        if device_name and device_name != 'null':
            total = 1
            instance = self.queryset.filter(name=device_name)
            ser_asset = self.serializer_class(instance=instance, many=True)
        else:
            total = self.queryset.count()
            page_list = page.paginate_queryset(self.queryset, request, view=self)
            # print(request.META.get('REMOTE_ADDR'))
            instance = page_list
            ser_asset = self.serializer_class(instance=instance, many=True)
        response['data'] = ser_asset.data
        response['msg'] = 'successful'
        response['total'] = total
        return Response(response)
