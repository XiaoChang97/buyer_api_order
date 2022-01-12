
import allure
import pytest
from py_page.base_api import BaseApi
from common.log import Logger
from py_page.get_case import GetCase


logging = Logger(__name__).get_logger()
class TestTemple(BaseApi):
	# 读取测试用例，以list形式返回：('.\yaml_test_api\buyer_login.yaml',test_login)
	case_list = GetCase()
	params:list = case_list.get_yaml_case()
	@pytest.mark.parametrize('path,api',params)
	def test_case_temple(self, path, api):
		yaml_api_datas = BaseApi.read_yaml(path,api)
		logging.info(f'************测试用例开始执行测试接口****************')
		logging.info(f'用例yaml文件路径：{path}，用例名称：{api}************')
		with allure.step(f"对接口【{path}:{api}】进行测试"):
			res = self.make_keys_requests(path, api)
			result = res
			logging.info(f'测试用例中获取到的接口实际响应result为{result}')
			exc = self.json_res(yaml_api_datas,'$..except')[0]  #获取yaml中接口的期望值返回一个字典
			logging.info(f'测试用例中从yaml中获取到的期望值exc为{exc}')
			self.assert_res(res=result, exc=exc)

if __name__ == '__main__':
	TestTemple()