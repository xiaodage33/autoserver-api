from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView

from backend.utils.page import Page
from repository import models
from backend.cmdbSerializers.common_serializers import ServerSerializer


class Server(ViewSetMixin, APIView):
    queryset = models.Server.objects.all().order_by('-asset__latest_date')
    serializer_class = ServerSerializer

    def list(self, request, *args, **kwargs):
        print(request.META.get('HTTP_X_TOKEN'))
        response = {'code': 20000, 'msg': None, 'data': None}
        hostname = request.query_params.get('hostname')
        # device_status_id = int(request.query_params.get('device_status_id'))
        page = Page()
        if hostname and hostname != 'null':
            total = 1
            instance = self.queryset.filter(hostname=hostname)
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
