import os
import warnings
import numpy as np
from cmd_color import ColorOutput
import time
from image_utils import to_binary
import cv2


_print = ColorOutput()._print


class ADBHelper():
    """ 调用 adb 相关的功能
    """

    def __init__(self, local_host=None):
        if local_host is None:
            self.__local_host = '127.0.0.1:7555' # 默认使用 MuMu 的端口

        else:
            self.__local_host = local_host

        if ':' not in self.__local_host:
            warnings.warn('port should be specified, use default port `7555`.')
            self.__local_host += ':7555'

        result = os.system('adb connect ' + self.__local_host + ' 1>nul 2>nul')
        if result:
            raise Exception('can not connect to {}, error code {}'.format(self.__local_host, result))
        else:
            _print('成功连接至 {}'.format(self.__local_host), 'green')

        self.__screen_shot_save_dir = 'screen' # 截图的存放目录
        if not self.__screen_shot_save_dir:
            os.mkdir(self.__screen_shot_save_dir)



    def _get_screen_shot(self, filename, save_dir='./screen'):
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        try:
            if '.jpg' in filename or '.png' in filename:
                os.system('adb shell screencap -p /sdcard/' + filename + ' 1>nul 2>nul')
                os.system('adb pull /sdcard/' + filename + ' ' + save_dir + ' 1>nul 2>nul')
                return os.path.join(save_dir, filename)
            else:
                os.system('adb shell screencap -p /sdcard/' + filename + '.png' + ' 1>nul 2>nul')
                os.system('adb pull /sdcard/' + filename + '.png ' + save_dir + ' 1>nul 2>nul')
                return os.path.join(save_dir, filename + '.png')
        except:
            raise Exception('can not get screen shot')


    def _click(self, x, y, epsilon=None, delay=None):
        """ 模拟点击屏幕
        args:
            epsilon: 随机在 (x, y) 附近浮动 epsilon 个像素
            delay: 点击后等待的时间
        """

        if epsilon is not None:
            x += np.random.randint(-epsilon, epsilon)
            y += np.random.randint(-epsilon, epsilon)

        os.system('adb shell input tap {} {} 1>nul 2>nul'.format(x, y))

        if delay:
            time.sleep(delay)


    def _swipe(self, x1, y1, x2, y2, delta=None, delay=None):
        """ 模拟滑动屏幕
        args:
            delta: 模拟滑动的时间
            delay: 滑动完成后等待的时间
        """

        if delta is None:
            os.system('adb shell input swipe {} {} {} {} 1>nul 2>nul'.format(x1, y1, x2, y2))
        else:
            os.system('adb shell input swipe {} {} {} {} {} 1>nul 2>nul'.format(x1, y1, x2, y2, delta))

        if delay:
            time.sleep(delay)


    def _get_screen(self, filename, bin=True):
        """ 返回屏幕的截图
        args:
            bi: True 时返回图片的二值化
        """

        self._get_screen_shot(filename)
        img = cv2.imread(os.path.join(self.__screen_shot_save_dir, filename))
        if bin:
            img = to_binary(img)
        return img
