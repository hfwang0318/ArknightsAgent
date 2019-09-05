from arknights.config import MissionLocConf, MissionTypeConf, MoveConf, PageConf
from arknights.resolution_map import ResolutionMap
import operator
import os
import cv2
from image_utils import to_binary
import numpy as np
import time


class PageSelector():
    def __init__(self, _map, adb_helper, detector, checker):
        self.__adb_helper = adb_helper
        self.__detector = detector
        self.__map = _map
        self.__checker = checker

        self.__screen_shot_save_dir = 'screen' # 截图的存放目录
        if not self.__screen_shot_save_dir:
            os.mkdir(self.__screen_shot_save_dir)


    def _go(self, mission):
        target = self._get_mission_page(mission)

        self._auto_move_to_target_page(target)

        self._to_left()
        self._to_delta_right(self._get_move_times(mission))

        if self.__map._item_coords[mission]['type'] == 'bbox':
            bbox = self.__map._get_coord(mission)
            x = np.random.randint(bbox[0], bbox[2], size=1)[0]
            y = np.random.randint(bbox[1], bbox[3], size=1)[0]
            self.__adb_helper._click(x, y)
        else:
            x, y = self.__map._get_coord(mission)
            self.__adb_helper._click(x, y, epsilon=5, delay=2)


    def _get_mission_page(self, mission):
        """ 返回要刷的关卡所在页面
        """

        for k, v in MissionLocConf._all_missions.items():
            if mission in v:
                return k


    def _move_to_target_page(self, target, cur):
        """ 移动到目标页面
        """

        if cur is None:
            raise Exception('not detect current page')

        if cur == target:
            return

        if cur != target and cur != PageConf._main_page:
            self.__adb_helper._click(self.__map._item_coords['menu']['coord'][0],
                                     self.__map._item_coords['menu']['coord'][1],
                                     epsilon=5,
                                     delay=1)

            self.__adb_helper._click(self.__map._item_coords['home']['coord'][0],
                                     self.__map._item_coords['home']['coord'][1],
                                     epsilon=5,
                                     delay=1)

            self._move_to_target_page(target, PageConf._main_page)

        if cur == PageConf._main_page:
            steps = self._get_route(target)
            for step in steps:
                self.__adb_helper._click(step[0], step[1], epsilon=5, delay=1)


    def _get_route(self, target):
        """ 返回从主页面到目标页面的点击逻辑
        """

        if operator.eq(self.__map.resolution, [1600, 900]):
            self.__route_huolan_stage_1 = [[1480, 225],
                                           [1400, 425]]

            self.__route_huolan_stage_2 = [[1480, 225],
                                           [1360, 535]]


            # 物资筹备和芯片搜索中子关卡顺序坐标
            self.__route_wuzi_order = {1: [[240, 625]],
                                       2: [[570, 620]],
                                       3: [[910, 620]],
                                       4: [[1245, 620]],
                                       5: [[1535, 625]]}

            self.__route_wuzi_base = [[1220, 255],
                                      [300, 835]]

            self.__route_xinpian_base = [[1220, 255],
                                         [490, 835]]

            self.__route_xinpian_order = {1: [300, 625],
                                          2: [640, 625],
                                          3: [970, 625],
                                          4: [1310, 625]}

            self.__route_jiaomie = [[1220, 255],
                                    [680, 835],
                                    [255, 430]]

            self.__route_zhuxian_base = [[1220, 255]]


            if target == PageConf._activate_battle_select_huolan_stage_1:
                return self.__route_huolan_stage_1

            elif target == PageConf._activate_battle_select_huolan_stage_2:
                return self.__route_huolan_stage_2

            elif target == PageConf._wuzi_page:
                return self.__route_wuzi_base

            elif target == PageConf._xinpian_page:
                return self.__route_xinpian_base

            elif target == PageConf._zhanshu_page:
                order = self.__checker._check_wuzi_order()
                route = self.__route_wuzi_order[order[PageConf._zhanshu_page]]
                return route

            elif target == PageConf._kongzhong_page:
                order = self.__checker._check_wuzi_order()
                route = self.__route_wuzi_order[order[PageConf._kongzhong_page]]
                return route

            elif target == PageConf._ziyuan_page:
                order = self.__checker._check_wuzi_order()
                route = self.__route_wuzi_order[order[PageConf._ziyuan_page]]
                return route

            elif target == PageConf._fensui_page:
                order = self.__checker._check_wuzi_order()
                route = self.__route_wuzi_order[order[PageConf._fensui_page]]
                return route

            elif target == PageConf._huowu_page:
                order = self.__checker._check_wuzi_order()
                route = self.__route_wuzi_order[order[PageConf._huowu_page]]
                return route

            elif target == PageConf._guruojintang_page:
                order = self.__checker._check_xinpian_order()
                route = self.__route_xinpian_order[order[PageConf._guruojintang_page]]
                return route

            elif target == PageConf._cuikulaxiu_page:
                order = self.__checker._check_xinpian_order()
                route = self.__route_xinpian_order[order[PageConf._cuikulaxiu_page]]
                return route

            elif target == PageConf._shibukedang_page:
                order = self.__checker._check_xinpian_order()
                route = self.__route_xinpian_order[order[PageConf._shibukedang_page]]
                return route

            elif target == PageConf._shenxianshizu_page:
                order = self.__checker._check_xinpian_order()
                route = self.__route_xinpian_order[order[PageConf._shenxianshizu_page]]
                return route

            elif target == PageConf._jiaomie_page:
                return self.__route_jiaomie

            elif target == PageConf._zhuxian_page:
                return self.__route_zhuxian_base




    def _get_location(self):
        """ 获取当前所处页面
        """

        self._to_left()
        img = self.__adb_helper._get_screen('page_detect.png', bin=True)

        img_paths = []
        for k, v in self.__map._item_coords.items():
            coord = v['coord']

            if v['type'] == 'bbox':
                x1, y1, x2, y2 = coord

                img_patch = img[y1: y2, x1: x2]
                img_patch = self.__checker._check_img(img_patch)

                save_path = os.path.join(self.__screen_shot_save_dir, k + '.png')
                # cv2.imwrite(save_path, img_patch)
                cv2.imencode('.png', img_patch)[1].tofile(save_path)
                img_paths.append(save_path)

        detect_result_paths = []
        for img_path in img_paths:
            save_path = os.path.join(self.__screen_shot_save_dir, img_path.split('\\')[-1].split('.')[0])
            self.__detector._detect(filepath=img_path, save_path=save_path)

            detect_result_paths.append(save_path + '.txt')

        cur_page = None
        for result in detect_result_paths:
            result = self.__detector._get_result(result)

            if '作战' in result:
                cur_page = PageConf._main_page
                break

            elif '主舞台' in result:
                cur_page = PageConf._activate_huolan_page
                break

            elif 'OF-1' in result:
                cur_page = PageConf._activate_battle_select_huolan_stage_1
                break

            elif 'OF-F4' in result:
                cur_page = PageConf._activate_battle_select_huolan_stage_2
                break

            elif 'LS-1' in result:
                cur_page = PageConf._zhanshu_page
                break

            elif 'CA-1' in result:
                cur_page = PageConf._kongzhong_page
                break

            elif 'SK-1' in result:
                cur_page = PageConf._ziyuan_page
                break

            elif 'AP-1' in result:
                cur_page = PageConf._fensui_page
                break

            elif 'CE-1' in result:
                cur_page = PageConf._huowu_page
                break

            elif 'PR-A-1' in result:
                cur_page = PageConf._guruojintang_page
                break

            elif 'PR-B-1' in result:
                cur_page = PageConf._cuikulaxiu_page
                break

            elif 'PR-C-1' in result:
                cur_page = PageConf._shibukedang_page
                break

            elif 'PR-D-1' in result:
                cur_page = PageConf._shenxianshizu_page
                break

            elif '龙门市区' in result:
                cur_page = PageConf._jiaomie_page
                break

            elif '黑暗时代' in result:
                cur_page = PageConf._zhuxian_page
                break

            elif '0-2' in result:
                cur_page = PageConf._zhuxian_0_page
                break

            elif '1-2' in result:
                cur_page = PageConf._zhuxian_1_page
                break

            elif '2-1' in result:
                cur_page = PageConf._zhuxian_2_page
                break

            elif '3-1' in result:
                cur_page = PageConf._zhuxian_3_page
                break

            elif '4-3' in result:
                cur_page = PageConf._zhuxian_4_page
                break

            elif '5-2' in result:
                cur_page = PageConf._zhuxian_5_page
                break

            else:
                cur_page = -1

        return cur_page


    def _get_move_times(self, mission):
        """ 返回当前任务需要向右滑动屏幕的次数
        """

        return MoveConf._move_times[mission]


    def _auto_move_to_target_page(self, target):
        """ 自动跳转到目标页面
        """

        t0 = time.time()
        cur_page = self._get_location()
        print('detect picture cost time {}'.format(time.time() - t0))
        print('cur page {} target {}'.format(cur_page, target))

        target_type = self.__checker._check_target_type(target)

        if target_type == MissionTypeConf._type_zhuxian_0:
            self._move_to_target_page(PageConf._zhuxian_page, cur_page)
            self._to_left()
            self._to_delta_right(0)
            x, y = self.__map._get_coord('chap_0')
            self.__adb_helper._click(x, y, epsilon=10, delay=2)

        elif target_type == MissionTypeConf._type_zhuxian_1:
            self._move_to_target_page(PageConf._zhuxian_page, cur_page)
            self._to_left()
            self._to_delta_right(1)
            x, y = self.__map._get_coord('chap_1')
            self.__adb_helper._click(x, y, epsilon=10, delay=2)

        elif target_type == MissionTypeConf._type_zhuxian_2:
            self._move_to_target_page(PageConf._zhuxian_page, cur_page)
            self._to_left()
            self._to_delta_right(1)
            x, y = self.__map._get_coord('chap_2')
            self.__adb_helper._click(x, y, epsilon=10, delay=2)

        elif target_type == MissionTypeConf._type_zhuxian_3:
            self._move_to_target_page(PageConf._zhuxian_page, cur_page)
            self._to_left()
            self._to_delta_right(1)
            x, y = self.__map._get_coord('chap_3')
            self.__adb_helper._click(x, y, epsilon=10, delay=2)

        elif target_type == MissionTypeConf._type_zhuxian_4:
            self._move_to_target_page(PageConf._zhuxian_page, cur_page)
            self._to_left()
            self._to_delta_right(2)
            x, y = self.__map._get_coord('chap_4')
            self.__adb_helper._click(x, y, epsilon=10, delay=2)

        elif target_type == MissionTypeConf._type_zhuxian_5:
            self._move_to_target_page(PageConf._zhuxian_page, cur_page)
            self._to_left()
            self._to_delta_right(3)
            x, y = self.__map._get_coord('chap_5')
            self.__adb_helper._click(x, y, epsilon=10, delay=2)

        elif target_type == MissionTypeConf._type_wuzi:
            self._move_to_target_page(PageConf._wuzi_page, cur_page)
            x, y = self._get_route(target)
            self.__adb_helper._click(x, y, epsilon=5)

        elif target_type == MissionTypeConf._type_xinpian:
            self._move_to_target_page(PageConf._xinpian_page, cur_page)
            x, y = self._get_route(target)
            self.__adb_helper._click(x, y, epsilon=5)

        elif target_type == MissionTypeConf._type_jiaomie:
            self._move_to_target_page(target, cur=cur_page)

        elif target_type == MissionTypeConf._type_active:
            self._move_to_target_page(target, cur_page)



    def _to_left(self):
        """ 移动到地图最左边
        """

        self.__adb_helper._swipe(0, 300, 2*self.__map.resolution[0], 300, delay=0.5)


    def _to_delta_right(self, times=1):
        """ 向右移动一段固定距离
        """

        if times == 0:
            return

        for _ in range(times):
            self.__adb_helper._swipe(800, 300, 0, 300, delta=5000, delay=0.5)
