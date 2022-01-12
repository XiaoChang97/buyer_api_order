import os.path
import traceback
import yaml
from common.log import Logger
from py_page.base_api import BaseApi

logging = Logger(__name__).get_logger()
class GetCase(BaseApi):

    #config_path = r'.\common\config.yaml'
    file = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(file,r'common\config.yaml')
    #返回config.yaml文件用例部分，字典类型
    config_case_data = BaseApi.read_yaml(config_path, 'get_case')
    #分别获取config_case_data中的value
    #path_list:['.\yaml_test_api\buyer_login.yaml','.\yaml_test_api\goods.yaml','.\yaml_test_api\order.yaml']
    path_list = config_case_data['case_path']
    tag = config_case_data['case_tag']

    def get_yaml_case(self, yaml_path_list:list=path_list, tag=tag):
        api_names = list() # 定义一个空列表，用于存放要执行的接口用例，供test_case_temple方法调用
        #遍历执行不同模块的testcase.yaml文件
        for yaml_path in yaml_path_list:
            try:
                yaml_path = os.path.join(self.file, yaml_path[2:])
                with open(yaml_path, "r", encoding="UTF-8") as f:
                    yaml_datas = yaml.safe_load(f)  # 获取整个yaml全部数据，返回一个字典对象
                    # 遍历具体yaml文件中的测试用例
                    for name in yaml_datas.keys():
                        yaml_is_skip = yaml_datas[name]['is_skip']  # 获取yaml文件中对应接口的is_skip标签字段
                        if yaml_is_skip != 0 : # 判断该接口用例is_skip字段是否为0，如果为0则跳过执行
                            if tag: # 当tag被指定，则获取yaml中的tag字段
                                yaml_tag = yaml_datas[name]['tag']  # 获取yaml文件中对应接口的tag标签字段
                                if tag == yaml_tag: # 如果指定的tag与yaml中的tag一致时，把该接口用例加入执行列表（即从yaml中筛选指定的用例）
                                    api_names.append((yaml_path, name))
                                else: # 接口用例中tag为非指定的tag时跳过执行
                                    pass
                            else: # 当tag未指定时默认执行yaml文件中所有接口测试用例
                                api_names.append((yaml_path, name))
                        else:
                            logging.info(f'测试用例:{yaml_path},{name} is_skip={yaml_is_skip} 跳过执行')
            except Exception as e:
                error_info = traceback.format_exc()
                logging.error(f"读取YAML文件:{yaml_path}把测试用例加入执行列表出错:{e}::错误详情:{error_info}")
                raise e
        return api_names






if __name__ == '__main__':
   pass