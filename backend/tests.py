from django.test import TestCase

# Create your tests here.
from rest_framework.views import APIView
from django.http import JsonResponse


def test_get_info(request):
    response = {
        'code': 20000,
        'data': {
            # 'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            'avatar': 'http://127.0.0.1:8000/static/avatar.gif',
            'introduction': "I am a super administrator",
            'name': "CMDB系统",
            'roles': ['admin', ]
        }
    }
    # response={'code':20000}
    return JsonResponse(response)
