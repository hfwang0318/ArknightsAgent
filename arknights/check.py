import numpy as np
import os
import operator
from arknights.config import PageConf, MissionTypeConf
import cv2
from arknights.resolution_map import ResolutionMap
from cmd_color import ColorOutput
import time



class Checker():
    def __init__(self, use_mixture, use_stone, n_mixture, n_stone, detector, _map, adb_helper):
        self.__detector = detector
        self.__use_mixture = use_mixture
        self.__use_stone = use_stone
        self.__n_mixture = n_mixture
        self.__n_stone = n_stone
        self.__map = _map
        self.__adb_helper = adb_helper

        self.__print = ColorOutput()

        self.__wuzi_list = {PageConf._fensui_page: '粉碎',
                            PageConf._zhanshu_page: '战术',
                            PageConf._ziyuan_page: '资源',
                            PageConf._huowu_page: '货物',
                            PageConf._kongzhong_page: '空中'}

        self.__xinpian_list = {PageConf._cuikulaxiu_page: '摧枯',
                               PageConf._shibukedang_page: '势不',
                               PageConf._shenxianshizu_page: '身先',
                               PageConf._guruojintang_page: '固若'}

        self.__screen_shot_save_dir = 'screen' # 截图的存放目录
        if not self.__screen_shot_save_dir:
            os.mkdir(self.__screen_shot_save_dir)


    def _check_wuzi_order(self):
        """ 返回当天物资筹备关卡顺序
        """

        img = self.__adb_helper._get_screen('check_wuzi_order.png')

        x1, y1, x2, y2 = self.__map._get_coord('wuzi_list')
        img_patch = img[y1: y2, x1: x2]
        img_patch = self._check_img(img_patch)

        # 去除图中间的黑方块
        shadow = np.mean(img_patch, axis=0)
        img_patch[:, shadow<=10] = 255

        cv2.imwrite(os.path.join(self.__screen_shot_save_dir, 'check_wuzi_order.png'), img_patch)

        self.__detector._detect(os.path.join(self.__screen_shot_save_dir, 'check_wuzi_order.png'),
                                os.path.join(self.__screen_shot_save_dir, 'check_wuzi_order'))

        result = self.__detector._get_result(os.path.join(self.__screen_shot_save_dir, 'check_wuzi_order.txt'))
        order = {}
        for k, v in self.__wuzi_list.items():
            order[k] = result.find(v)
        order = dict(sorted(order.items(), key=operator.itemgetter(1)))
        for i, k in enumerate(list(order.keys())):
            order[k] = i+1

        return order


    def _check_xinpian_order(self):
        """ 返回当天芯片搜索关卡顺序
        """

        img = self.__adb_helper._get_screen('check_xinpian_order.png')

        x1, y1, x2, y2 = self.__map._get_coord('xinpian_list')
        img_patch = img[y1: y2, x1: x2]
        img_patch = self._check_img(img_patch)

        # 去除图中间的黑方块
        shadow = np.mean(img_patch, axis=0)
        img_patch[:, shadow<=10] = 255

        cv2.imwrite(os.path.join(self.__screen_shot_save_dir, 'check_xinpian_order.png'), img_patch)

        self.__detector._detect(os.path.join(self.__screen_shot_save_dir, 'check_xinpian_order.png'),
                                os.path.join(self.__screen_shot_save_dir, 'check_xinpian_order'))

        result = self.__detector._get_result(os.path.join(self.__screen_shot_save_dir, 'check_xinpian_order.txt'))
        order = {}
        for k, v in self.__xinpian_list.items():
            order[k] = result.find(v)
        order = dict(sorted(order.items(), key=operator.itemgetter(1)))
        for i, k in enumerate(list(order.keys())):
            order[k] = i+1
        return order


    def _check_img(self, img, pad=[[10, 10], [10, 10]], erosion=False):
        """ 检查图片是否为白底黑字, 若不是， 则转化为白底黑字
        为所有图片的各个边 pad 10个像素
        """

        assert len(img.shape) == 2, 'expect image have 2 dims, but got {}'.format(len(img.shape))

        # 通过图片最左边一列的平均像素值判断图片背景色
        if np.mean(img[:, 0]) < 175:
            _, img = cv2.threshold(img, 175, 255, cv2.THRESH_BINARY_INV)
        img = np.pad(img, pad, 'edge')

        if erosion:
            kernel = np.ones((3,3),np.uint8)
            img = cv2.erode(img, kernel, iterations=1)
        return img



    def _check_lizhi(self):
        """ 检测当前理智
        如果不足时，允许使用源石或理智合剂时自动使用
        """

        self.__print('正在检查当前剩余理智...@blue')

        img = self.__adb_helper._get_screen('check_lizhi.png', bin=True)

        x1, y1, x2, y2 = self.__map._get_coord('cur_lizhi')
        img_patch = img[y1: y2, x1: x2]
        img_patch = self._check_img(img_patch)

        cv2.imwrite(os.path.join(self.__screen_shot_save_dir, 'cur_lizhi.png'), img_patch)

        x1, y1, x2, y2 = self.__map._get_coord('lizhi_cost')
        img_patch = img[y1: y2, x1: x2]
        img_patch = self._check_img(img_patch)

        cv2.imwrite(os.path.join(self.__screen_shot_save_dir, 'lizhi_cost.png'), img_patch)

        self.__detector._detect(os.path.join(self.__screen_shot_save_dir, 'cur_lizhi.png'),
                                os.path.join(self.__screen_shot_save_dir, 'cur_lizhi'))

        self.__detector._detect(os.path.join(self.__screen_shot_save_dir, 'lizhi_cost.png'),
                                os.path.join(self.__screen_shot_save_dir, 'lizhi_cost'))

        cur_lizhi = np.abs(int(self.__detector._get_result(os.path.join(self.__screen_shot_save_dir,
                                                                        'cur_lizhi.txt')).split('/')[0]))

        lizhi_cost = np.abs(int(self.__detector._get_result(os.path.join(self.__screen_shot_save_dir,
                                                                         'lizhi_cost.txt'))))

        self.__print('当前理智: {}@yellow'.format(cur_lizhi))

        if cur_lizhi < lizhi_cost:
            if self.__use_mixture or self.__use_stone:
                bbox = self.__map._item_coords['start_1']['coord']
                x = np.random.randint(bbox[0], bbox[2], size=1)[0]
                y = np.random.randint(bbox[1], bbox[3], size=1)[0]
                self.__adb_helper._click(x, y, delay=0.5)

                is_recovery = False
                n_mixture = self._check_mixture()
                try:
                    n_mixture = int(n_mixture)
                except:
                    n_mixture = 0
                    self.__print('理智合剂不足@blue')

                if self.__use_mixture and n_mixture and self.__n_mixture:
                    self.__print('当前理智不足, 自动使用理智合剂@blue')

                    x, y = self.__map._get_coord('confirm_recovery_lizhi')
                    self.__adb_helper._click(x, y, epsilon=5)
                    self.__n_mixture -= 1
                    # self.__adb_helper._click(300, 300, epsilon=5)
                    is_recovery = True


                if self.__use_stone and not is_recovery and self.__n_stone:
                    self.__print('当前理智不足, 自动使用源石@blue')

                    if n_mixture > 0:
                        x, y = self.__map._get_coord('stone_btn')

                        self.__adb_helper._click(x, y, epsilon=5, delay=2)

                    img = self.__adb_helper._get_screen('check_2.png')

                    x1, y1, x2, y2 = self.__map._get_coord('n_stone')

                    img_patch = img[y1: y2, x1: x2]
                    img_patch = self._check_img(img_patch)

                    cv2.imwrite(os.path.join(self.__screen_shot_save_dir, 'n_stone.png'), img_patch)

                    self.__detector._detect(os.path.join(self.__screen_shot_save_dir, 'n_stone.png'),
                                            os.path.join(self.__screen_shot_save_dir, 'n_stone'))

                    n_stone = self.__detector._get_result(os.path.join(self.__screen_shot_save_dir, 'n_stone.txt'))

                    try:
                        n_stone = int(n_stone)
                        if n_stone > 0:
                            x, y = self.__map._get_coord('confirm_recovery_lizhi')
                            self.__adb_helper._click(x, y, epsilon=5)
                            self.__n_stone -= 1
                            is_recovery = True
                    except:
                        self.__print('源石不足，代理结束@green')

                if not is_recovery:
                    self.__print('理智合剂或源石不足，代理结束@green')
                    return False
                time.sleep(2)
                return True
            else:
                self.__print('当前理智不足，代理结束@green')
                return False
        return True


    def _check_mixture(self):
        """ 检查当前理智药剂数量
        """

        img = self.__adb_helper._get_screen('check_1.png', bin=True)

        x1, y1, x2, y2 = self.__map._get_coord('n_mixture')

        img_patch = img[y1: y2, x1: x2]
        img_patch = self._check_img(img_patch)

        cv2.imwrite(os.path.join(self.__screen_shot_save_dir, 'n_mixture.png'), img_patch)

        self.__detector._detect(os.path.join(self.__screen_shot_save_dir, 'n_mixture.png'),
                                os.path.join(self.__screen_shot_save_dir, 'n_mixture'))

        n_mixture = self.__detector._get_result(os.path.join(self.__screen_shot_save_dir, 'n_mixture.txt'))
        return n_mixture


    def _check_agent_command(self):
        """ 检查代理指挥
        若未开启则自动开启
        """

        img = self.__adb_helper._get_screen('check_agent.png', bin=False)

        x, y = self.__map._get_coord('agent_select')

        if np.mean(img[y, x]) < 175:
            self.__print('当前未设置代理指挥，自动设置...@blue')
            self.__adb_helper._click(x, y, epsilon=3)


    def _check_target_type(self, target):
        """ 返回目标的类型，类型包括 `主线`, `物资筹备`, `芯片搜索`, `剿灭作战`, `活动`, [待补充...
        """

        if target in [PageConf._zhanshu_page,
                      PageConf._fensui_page,
                      PageConf._ziyuan_page,
                      PageConf._kongzhong_page,
                      PageConf._huowu_page]:
            return MissionTypeConf._type_wuzi

        elif target in [PageConf._guruojintang_page,
                        PageConf._cuikulaxiu_page,
                        PageConf._shibukedang_page,
                        PageConf._shenxianshizu_page]:
            return MissionTypeConf._type_xinpian

        elif target in [PageConf._jiaomie_page]:
            return MissionTypeConf._type_jiaomie

        elif target in [PageConf._activate_battle_select_huolan_stage_1,
                        PageConf._activate_battle_select_huolan_stage_2,
                        PageConf._activate_huolan_page]:
            return MissionTypeConf._type_active

        elif target in [PageConf._zhuxian_0_page]:
            return MissionTypeConf._type_zhuxian_0

        elif target in [PageConf._zhuxian_1_page]:
            return MissionTypeConf._type_zhuxian_1

        elif target in [PageConf._zhuxian_2_page]:
            return MissionTypeConf._type_zhuxian_2

        elif target in [PageConf._zhuxian_3_page]:
            return MissionTypeConf._type_zhuxian_3

        elif target in [PageConf._zhuxian_4_page]:
            return MissionTypeConf._type_zhuxian_4

        elif target in [PageConf._zhuxian_5_page]:
            return MissionTypeConf._type_zhuxian_5