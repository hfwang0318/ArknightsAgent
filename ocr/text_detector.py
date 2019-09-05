import os
import warnings


class Tesseract():
    def __init__(self, lang=None, oem=None, tessdata_dir=None, psm=6):
        self.__lang = lang
        self.__tessdata_dir = tessdata_dir
        self.__oem = str(oem)
        self.__psm = str(psm)
        
        if self.__lang is None:
            self.__lang = 'chi_sim'
            warnings.warn('detect language should be specified, use default `chi_sim`')
        
        if self.__oem is None:
            self.__oem = 0
            warnings.warn('if oem not be specified, we use default `0`')
    
    def _set_psm(self, psm):
        self.__psm = str(psm)
        
        
    def _detect(self, filepath, save_path):
        if self.__tessdata_dir is None:
            os.system('tesseract ' + filepath + ' ' + save_path + ' -l ' + self.__lang + ' --oem ' + self.__oem + ' --psm ' + self.__psm + ' 1>nul 2>nul')
        else:
            os.system('tesseract ' + '--tessdata-dir ' + self.__tessdata_dir + ' ' + filepath + ' ' + \
                save_path + ' -l ' + self.__lang + ' --oem ' + self.__oem + ' --psm ' + self.__psm + ' 1>nul 2>nul')
            
    
    def _get_result(self, filepath):
        with open(filepath, 'rb') as f:
            result = f.readlines()
            result = [i.decode() for i in result]
            result = ''.join(result)
            result = result.strip()
            result = result.replace(' ', '')
            return result