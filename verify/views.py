from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from verify.response import *
from verify.utils.localVerifyCode import verify


class VerifyBase64View(GenericViewSet):
    """
    识别验证码接口
    """
    def verify(self, request):
        """
        返回返回坐标
        :return:
        """
        imageFile = request.data.get("imageFile")
        if not imageFile:
            return VERIFY_NOT_BASE64
        result = verify(imageFile)
        VERIFY_SUCC["data"] = result
        return Response(VERIFY_SUCC)
