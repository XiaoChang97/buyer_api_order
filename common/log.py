import logging
import time
import os

class Logger:
    def __init__(self, name, logger_level='INFO', stream_level='INFO', file_level='INFO'):

        # 创建一个 logger
        self.__logger = logging.getLogger(name)
        # 设置Log等级总开关
        self.__logger.setLevel(logger_level)
        # 创建 handler，用于日志写入
        currTime = time.strftime("%Y-%m-%d") # 获取日期年-月-日
        log_py_path = os.path.abspath(__file__) # 当前py文件的绝对路径,会定位到对应py文件
        log_dir_path = os.path.split(log_py_path)[0] # 当前py文件的文件夹路径
        pro_path = os.path.dirname(log_dir_path) # 当前py文件对应文件夹的上层目录路径
        Log_path = pro_path + '\\Logs\\'
        log_name = Log_path + currTime + '.log'
        fh = logging.FileHandler(log_name, mode='a')  # mode = 'a' 为在原日志上追加，'w'为覆盖 输出日志到文件
        fh.setLevel(file_level) # 输出到 file 的日志等级
        ch = logging.StreamHandler() # 输出日志到控制台
        ch.setLevel(stream_level) # 输出到控制台的日志等级
        # 定义日志handler的输出格式
        fmt = logging.Formatter('%(asctime)s - %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s')
        fh.setFormatter(fmt)
        ch.setFormatter(fmt)

        # 添加 logger 到 handler里面
        self.__logger.addHandler(fh)
        self.__logger.addHandler(ch)


    def get_logger(self):
        return self.__logger