from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView

from backend.utils.page import Page
from repository import models
from backend.cmdbSerializers.common_serializers import UserProfileSerializer


class UserList(ViewSetMixin, APIView):
    queryset = models.UserProfile.objects.all().order_by('-username')
    serializer_class = UserProfileSerializer
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        response = {'code': 20000, 'msg': None, 'data': None}
        # device_status_id = int(request.query_params.get('device_status_id'))
        page = Page()
        total = self.queryset.count()
        page_list = page.paginate_queryset(self.queryset, request, view=self)
        # print(request.META.get('REMOTE_ADDR'))
        instance = page_list
        ser_user_list = self.serializer_class(instance=instance, many=True)
        response['data'] = ser_user_list.data
        response['msg'] = 'successful'
        response['total'] = total
        return Response(response)
