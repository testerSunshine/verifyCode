import os

import numpy as np
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from verify.response import *
from verify.utils import pretreatment
from verify.utils.localVerifyCode import base64_to_image, get_text
import tensorflow as tf
from keras import models

from verify.utils.mlearn_for_image import preprocess_input

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

graph = tf.get_default_graph()


def load_keras_model():
    global textModel
    textModel = models.load_model(PATH('utils/model.v2.0.h5'))
    global imgModel
    imgModel = models.load_model(PATH('utils/12306.image.model.h5'))


load_keras_model()


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
        verify_titles = ['打字机', '调色板', '跑步机', '毛线', '老虎', '安全帽', '沙包', '盘子', '本子', '药片', '双面胶', '龙舟', '红酒', '拖把', '卷尺',
                         '海苔', '红豆', '黑板', '热水袋', '烛台', '钟表', '路灯', '沙拉', '海报', '公交卡', '樱桃', '创可贴', '牌坊', '苍蝇拍', '高压锅',
                         '电线', '网球拍', '海鸥', '风铃', '订书机', '冰箱', '话梅', '排风机', '锅铲', '绿豆', '航母', '电子秤', '红枣', '金字塔', '鞭炮',
                         '菠萝', '开瓶器', '电饭煲', '仪表盘', '棉棒', '篮球', '狮子', '蚂蚁', '蜡烛', '茶盅', '印章', '茶几', '啤酒', '档案袋', '挂钟',
                         '刺绣',
                         '铃铛', '护腕', '手掌印', '锦旗', '文具盒', '辣椒酱', '耳塞', '中国结', '蜥蜴', '剪纸', '漏斗', '锣', '蒸笼', '珊瑚', '雨靴',
                         '薯条',
                         '蜜蜂', '日历', '口哨']
        # 读取并预处理验证码
        img = base64_to_image(imageFile)
        text = get_text(img)
        imgs = np.array(list(pretreatment._get_imgs(img)))
        imgs = preprocess_input(imgs)
        text_list = []
        # 识别文字
        global graph
        with graph.as_default():
            label = textModel.predict(text)
        label = label.argmax()
        text = verify_titles[label]
        text_list.append(text)
        # 获取下一个词
        # 根据第一个词的长度来定位第二个词的位置
        if len(text) == 1:
            offset = 27
        elif len(text) == 2:
            offset = 47
        else:
            offset = 60
        text = get_text(img, offset=offset)
        if text.mean() < 0.95:
            with graph.as_default():
                label = textModel.predict(text)
            label = label.argmax()
            text = verify_titles[label]
            text_list.append(text)
        print("题目为{}".format(text_list))
        # 加载图片分类器
        with graph.as_default():
            labels = imgModel.predict(imgs)
        labels = labels.argmax(axis=1)
        results = []
        for pos, label in enumerate(labels):
            l = verify_titles[label]
            print(pos + 1, l)
            if l in text_list:
                results.append(str(pos + 1))
        VERIFY_SUCC["data"] = results
        return Response(VERIFY_SUCC)


