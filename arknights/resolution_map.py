import operator
import support_resolution


# 添加新图时需改动
class ResolutionMap():
    def __init__(self, resolution):
        self.resolution = resolution

        support_resolution.is_valid(self.resolution)


    @property
    def _item_coords(self):
        """ 返回坐标格式 (x1, y1, x2, y2), 其中 x1, y1 表示左上角, x2, y2 表示右下角
        """

        if operator.eq(self.resolution, [1600, 900]):
            # 基础按键位置
            item_coords_base = {'battle': {'coord': (1130, 150, 1300, 250), 'type': 'bbox'}, # 主页面 `作战`
                                'agent': {'coord': (1420, 720, 1550, 760), 'type': 'bbox'}, # `代理指挥`
                                'agent_select': {'coord': (1335, 740), 'type': 'point'}, # `代理指挥` 选择按钮
                                'start_1': {'coord': (1400, 800, 1545, 840), 'type': 'bbox'}, # 第一个 `开始作战` 按钮
                                'start_2': {'coord': (1310, 585, 1450, 710), 'type': 'bbox'}, # 第二个 `开始作战` 按钮
                                'lizhi_cost': {'coord': (1485, 850, 1530, 875), 'type': 'bbox'}, # `理智消耗`
                                'cur_lizhi': {'coord': (1415, 25, 1590, 70), 'type': 'bbox'}, # `当前理智`
                                'mixture_btn': {'coord': (1000, 95), 'type': 'point'}, # `使用药剂恢复` 按钮
                                'stone_btn': {'coord': (1430, 95), 'type': 'point'}, # `使用源石恢复` 按钮
                                'n_mixture': {'coord': (920, 300, 960, 330), 'type': 'bbox'}, # 理智药剂数量
                                'n_stone': {'coord': (1480, 170, 1535, 210), 'type': 'bbox'}, # 源石数量
                                'confirm_recovery_lizhi': {'coord': (1365, 725), 'type': 'point'}, # 确定使用理智药或者源石
                                'menu': {'coord': (335, 50), 'type': 'point'}, # 主页菜单
                                'home': {'coord': (115, 215), 'type': 'point'}, # 首页
                                'complete': {'coord': (40, 725, 510, 850), 'type': 'bbox'}, # 行动结束
                                'wuzi_list': {'coord': (140, 590, 1575, 650), 'type': 'bbox'}, # 物资筹备页面下的子分类列表
                                'xinpian_list': {'coord': (200, 590, 1400, 645), 'type': 'bbox'}, # 芯片搜索页面下的子分类列表
                                'base_notify_1': {'coord': (1540, 115), 'type': 'point'},
                                'base_notify_2': {'coord': (1540, 175), 'type': 'point'},
                                'LS-1': {'coord': (210, 700, 290, 735), 'type': 'bbox'},
                                'LS-2': {'coord': (600, 655), 'type': 'point'},
                                'LS-3': {'coord': (850, 510), 'type': 'point'},
                                'LS-4': {'coord': (1050, 370), 'type': 'point'},
                                'LS-5': {'coord': (1180, 220), 'type': 'point'},
                                'CA-1': {'coord': (210, 700, 290, 735), 'type': 'bbox'},
                                'CA-2': {'coord': (600, 655), 'type': 'point'},
                                'CA-3': {'coord': (850, 510), 'type': 'point'},
                                'CA-4': {'coord': (1050, 370), 'type': 'point'},
                                'CA-5': {'coord': (1180, 220), 'type': 'point'},
                                'SK-1': {'coord': (210, 700, 290, 735), 'type': 'bbox'},
                                'SK-2': {'coord': (600, 655), 'type': 'point'},
                                'SK-3': {'coord': (850, 510), 'type': 'point'},
                                'SK-4': {'coord': (1050, 370), 'type': 'point'},
                                'SK-5': {'coord': (1180, 220), 'type': 'point'},
                                'AP-1': {'coord': (210, 700, 290, 735), 'type': 'bbox'},
                                'AP-2': {'coord': (600, 655), 'type': 'point'},
                                'AP-3': {'coord': (850, 510), 'type': 'point'},
                                'AP-4': {'coord': (1050, 370), 'type': 'point'},
                                'AP-5': {'coord': (1180, 220), 'type': 'point'},
                                'CE-1': {'coord': (210, 700, 290, 735), 'type': 'bbox'},
                                'CE-2': {'coord': (600, 655), 'type': 'point'},
                                'CE-3': {'coord': (850, 510), 'type': 'point'},
                                'CE-4': {'coord': (1050, 370), 'type': 'point'},
                                'CE-5': {'coord': (1180, 220), 'type': 'point'},
                                'PR-A-1': {'coord': (480, 540, 600, 580), 'type': 'bbox'},
                                'PR-A-2': {'coord': (1050, 325), 'type': 'point'},
                                'PR-B-1': {'coord': (435, 540, 550, 575), 'type': 'bbox'},
                                'PR-B-2': {'coord': (1075, 310), 'type': 'point'},
                                'PR-C-1': {'coord': (430, 500, 545, 540), 'type': 'bbox'},
                                'PR-C-2': {'coord': (1050, 330), 'type': 'point'},
                                'PR-D-1': {'coord': (455, 535, 570, 565), 'type': 'bbox'},
                                'PR-D-2': {'coord': (1050, 325), 'type': 'point'},
                                '龙门市区': {'coord': (1285, 470, 1405, 500), 'type': 'bbox'},
                                '切尔诺伯格': {'coord': (250, 325), 'type': 'point'},
                                '龙门外环': {'coord': (945, 620), 'type': 'point'},
                                'heian': {'coord': (330, 170, 510, 210), 'type': 'bbox'}, # `黑暗时代`字样
                                '0-2': {'coord': (1410, 520, 1470, 555), 'type': 'bbox'},
                                '1-2': {'coord': (1125, 415, 1185, 450), 'type': 'bbox'},
                                '2-1': {'coord': (1000, 525, 1065, 565), 'type': 'bbox'},
                                '3-1': {'coord': (770, 420, 830, 455), 'type': 'bbox'},
                                '4-3': {'coord': (1265, 415, 1325, 450), 'type': 'bbox'},
                                '5-2': {'coord': (1160, 390, 1225, 425), 'type': 'bbox'},
                                'chap_0': {'coord': (450, 465), 'type': 'point'},
                                'chap_1': {'coord': (1070, 465), 'type': 'point'},
                                'chap_2': {'coord': (845, 465), 'type': 'point'},
                                'chap_3': {'coord': (1340, 465), 'type': 'point'},
                                'chap_4': {'coord': (1250, 465), 'type': 'point'},
                                'chap_5': {'coord': (1200, 465), 'type': 'point'},
                                '3-8': {'coord': (1555, 285), 'type': 'point'},
                                '4-5': {'coord': (625, 300), 'type': 'point'},
                                'S4-1': {'coord': (580, 565), 'type': 'point'},
                                '4-2': {'coord': (1060, 570), 'type': 'point'},
                                '4-10': {'coord': (960, 430), 'type': 'point'},
                                '4-6': {'coord': (965, 430), 'type': 'point'},
                                '4-9': {'coord': (680, 430), 'type': 'point'},
                                '4-8': {'coord': (420, 320), 'type': 'point'},
                                '4-7': {'coord': (140, 430), 'type': 'point'},
                                '4-4': {'coord': (1365, 435), 'type': 'point'},
                                '5-8': {'coord': (1555, 455), 'type': 'point'},
                                '5-1': {'coord': (800, 510), 'type': 'point'},
                                '1-7': {'coord': (1430, 285), 'type': 'point'},
                                }

            # 活动相关
            # 火蓝之心 19/8/27 - 19/9/24
            item_coords_active = {'huolan': {'coord': (1320, 250, 1470, 300), 'type': 'bbox'}, # 火蓝之心
                                  'stage_1': {'coord': (1330, 405, 1440, 445), 'type': 'bbox'}, # 主舞台
                                  'stage_2': {'coord': (1300, 515, 1420, 560), 'type': 'bbox'}, # 嘉年华
                                  'stage_3': {'coord': (), 'type': None},
                                  'OF-5': {'coord': (55, 250, 145, 290), 'type': 'bbox'},
                                  'OF-6': {'coord': (430, 255, 525, 290), 'type': 'bbox'},
                                  'OF-7': {'coord': (1110, 405, 1200, 440), 'type': 'bbox'},
                                  'OF-8': {'coord': (1400, 540, 1490, 575), 'type': 'bbox'},
                                  'OF-F4': {'coord': (1215, 380, 1320, 410), 'type': 'bbox'},
                                  'OF-1': {'coord': (1050, 285, 1150, 330), 'type': 'bbox'},
                                  }

            item_coords = dict(item_coords_base, **item_coords_active)
            return item_coords


    def _get_coord(self, key, mtype=None):
        """ 返回按键坐标
        """

        if mtype is None:
            mtype = self._item_coords[key]['type']

        if mtype == 'bbox':
            x1, y1, x2, y2 = self._item_coords[key]['coord']
            return [x1, y1, x2, y2]

        elif mtype == 'point':
            x, y = self._item_coords[key]['coord']
            return [x, y]