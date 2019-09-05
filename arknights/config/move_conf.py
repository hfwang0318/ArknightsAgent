class MoveConf():
    """ 记录从任务所在页面的最左端至任务位置需滑动固定距离的次数
    """

    _move_times = {
        # 火蓝之心
        'OF-6': 3,
        '0F-7': 3,
        'OF-8': 3,
        'OF-F1': 0,
        'OF-F2': 0,
        'OF-F3': 0,
        'OF-F4': 0,

        # 物资筹备
        'LS-1': 0,
        'LS-2': 0,
        'LS-3': 0,
        'LS-4': 0,
        'LS-5': 0,
        'CA-1': 0,
        'CA-2': 0,
        'CA-3': 0,
        'CA-4': 0,
        'CA-5': 0,
        'SK-1': 0,
        'SK-2': 0,
        'SK-3': 0,
        'SK-4': 0,
        'SK-5': 0,
        'AP-1': 0,
        'AP-2': 0,
        'AP-3': 0,
        'AP-4': 0,
        'AP-5': 0,
        'CE-1': 0,
        'CE-2': 0,
        'CE-3': 0,
        'CE-4': 0,
        'CE-5': 0,

        # 芯片搜索
        'PR-A-1': 0,
        'PR-A-2': 0,
        'PR-B-1': 0,
        'PR-B-2': 0,
        'PR-C-1': 0,
        'PR-C-2': 0,
        'PR-D-1': 0,
        'PR-D-2': 0,

        # 剿灭作战
        '切尔诺伯格': 0,
        '龙门外环': 0,
        '龙门市区': 0,

        # 主线
        '0-1': 0,
        '3-8': 3, # 聚酸酯组, 聚酸酯块
        '4-5': 2, # 酮凝集组, 酮阵列
        'S4-1': 1, # 异铁组, 异铁块
        '4-2': 0, # 糖组, 糖聚块
        '4-10': 5, # 全新装置, 改量装置
        '4-6': 2, # 固源岩组, 提纯源岩
        '4-9': 4, # RMA70-12, RMA70-24
        '4-8': 4, # 研磨石, 五水研磨石
        '4-7': 4, # 轻锰矿, 三水锰矿
        '4-4': 1, # 扭转醇, 白马醇
        '5-8': 3, # 酮凝集组, 酮阵列
        '5-1': 0, # 固源岩组
    }