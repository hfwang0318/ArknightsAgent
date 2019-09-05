from adb import ADBHelper
from arknights.resolution_map import ResolutionMap
import numpy as np
from ocr import Tesseract
import time
import os
import cv2
import warnings
from cmd_color import ColorOutput
from arknights.page_select import PageSelector
from arknights.check import Checker



DEBUG = True


class Agent():
    """ 代理需要执行的任务
    """

    def __init__(self, missions, resolution=[1600, 900], check_lizhi=True,
                 local_host=None, tessdata_dir=None,
                 use_stone=False, use_mixture=False,
                 n_stone=None, n_mixture=None, plan=None, daily=None):
        os.system('cls')

        self.__missions = missions
        self.__resolution = resolution
        self.__local_host = local_host
        self.__tessdata_dir = tessdata_dir
        self.__use_stone = use_stone
        self.__use_mixture = use_mixture
        self.__n_stone = n_stone
        self.__n_mixture = n_mixture
        self.__check_lizhi = check_lizhi
        self.__plan = plan
        self.__daily = daily


        if use_stone and n_stone is None:
            warnings.warn('if not specified the number of stone to cost, \
                          default set to use `1` stone')
            self.__n_stone = 1

        if use_mixture and n_mixture is None:
            warnings.warn('if not specified the number of mixture to cost, \
                          default set to use `1` mixture')
            self.__n_mixture = 1

        self.__map = ResolutionMap(resolution)
        self.__detector = Tesseract(lang='chi_sim', oem=1, tessdata_dir=tessdata_dir, psm=6)
        self.__adb_helper = ADBHelper(local_host=local_host)

        self.__checker = Checker(self.__use_mixture,
                                 self.__use_stone,
                                 self.__n_mixture,
                                 self.__n_stone,
                                 self.__detector,
                                 self.__map,
                                 self.__adb_helper)

        self.__page_selector = PageSelector(self.__map, self.__adb_helper, self.__detector, self.__checker)

        self.__print = ColorOutput()

        self.__screen_shot_save_dir = 'screen' # 截图的存放目录
        if not self.__screen_shot_save_dir:
            os.mkdir(self.__screen_shot_save_dir)


    def _clear_buffer(self):
        """ 清空存放截图的文件夹
        """

        for i in os.listdir(self.__screen_shot_save_dir):
            os.remove(i)


    def _run(self):
        self.__print('启动代理...')
        self.__print('使用分辨率: {}'.format(self.__resolution))
        self.__print('当前模拟器端口: {}\n'.format(self.__local_host))

        self.__print('任务列表:')
        for k, v in self.__missions.items():
            self.__print('关卡: {}, 次数: {}@yellow'.format(k, v))

        # if self.__daily:
        #     self.__print('\n自动完成日常, 间隔: {}, 次数: {}@blue'.format())

        for mission, times in self.__missions.items():
            # 跳转到目标关卡位置
            self.__print('\n跳转至目标页面(第一次需检测大量图片，请等待)...@blue')

            self.__page_selector._go(mission)

            self.__print('检查代理指挥...@blue')
            self.__checker._check_agent_command()

            # 如果 times = -1, 表示刷该关卡至体力耗尽
            if times == -1:
                times = 99999

            for t in range(times):
                self.__print('正在执行任务: {}, 当前次数: {}, 剩余次数: {}@yellow'.format(mission, t+1, times-t-1))

                if self.__check_lizhi:
                    if not self.__checker._check_lizhi():
                        return

                self.__print('开始作战@blue')
                for i in range(2):
                    bbox = self.__map._item_coords['start_' + str(i+1)]['coord']
                    x = np.random.randint(bbox[0], bbox[2], size=1)[0]
                    y = np.random.randint(bbox[1], bbox[3], size=1)[0]
                    self.__adb_helper._click(x, y, delay=2)

                while True:
                    time.sleep(5)

                    # 剿灭作战有一个作战简报，需先点击一次屏幕再检测是否结束
                    if mission in ['切尔诺伯格', '龙门外环', '龙门市区']:
                        self.__adb_helper._click(300, 300, epsilon=10, delay=1)

                    img = self.__adb_helper._get_screen('complete_raw.png', bin=True)

                    x1, y1, x2, y2 = self.__map._get_coord('complete')

                    img = img[y1: y2, x1: x2]

                    img = self.__checker._check_img(img)

                    cv2.imwrite(os.path.join(self.__screen_shot_save_dir, 'complete.png'), img)

                    self.__detector._detect(filepath=os.path.join(self.__screen_shot_save_dir, 'complete.png'),
                                            save_path=os.path.join(self.__screen_shot_save_dir, 'complete'))

                    result = self.__detector._get_result(os.path.join(self.__screen_shot_save_dir, 'complete.txt'))

                    if '行动结束' in result:
                        self.__adb_helper._click(300, 300, epsilon=5)
                        self.__print('行动结束@green')
                        time.sleep(5)
                        break
            self.__print('任务列表完成，代理结束@green')
        if not DEBUG:
            self._clear_buffer()

        os.system(self.__plan)