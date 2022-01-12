import os
import traceback
import jsonpath
import requests
import yaml
from string import Template
from common.log import Logger

logging = Logger(__name__).get_logger()
class BaseApi:
    def request_api(self,method, api, params=None, data=None, json=None, headers=None, res_type='json', verify=False)->dict:
        '''
        基于requests的接口请求封装
        :param method: 接口请求方式get、post
        :param api: 接口请求地址
        :param params: 用于get请求中传入请求数据，接收一个字典类型
        :param data: 用于post请求中传入表单数据，接收一个字典类型
        :param json: post请求中用于传入json格式的请求数据，接收一个字典类型
        :param headers: 用于构造请求头信息，接收一个字典类型
        :param res_type: 指定响应报文类型json、text
        :param verify: 接收布尔值，默认False，即不对https请求SSL验证
        :return: 接口响应状态码，以及接口响应报文，返回一个字典类型
                例：{'status_code'：200, 'content':{'code':1, msg='登录成功','data':{xxxxx}}}
        '''
        host = "http://dev.chananchor.com"
        api_url = host+api
        res_dict = dict()
        if method == 'get':
            try:
                res = requests.session().get(url=api_url, params=params, headers=headers, verify=verify)
                if res_type == 'json':
                    res_content = res.json()
                else:
                    res_content = res.text
                res_dict['status_code'] = res.status_code
                res_dict['content'] = res_content
                return res_dict
            except Exception as e:
                error_info = traceback.format_exc()
                logging.error(f"接口::{api}::请求出错::{e},错误详情:{error_info}")
                raise e

        elif method == 'post':
            try:
                res = requests.session().post(url=api_url, data=data, json=json, headers=headers, verify=verify)
                logging.info(f'响应头：{res.headers}')
                if res_type == 'json':
                    res_content = res.json()
                else:
                    res_content = res.text
                res_dict['status_code'] = res.status_code
                res_dict['content'] = res_content
                return res_dict
            except Exception as e:
                error_info = traceback.format_exc()
                logging.error(f"接口::{api}::请求出错::{e},错误详情:{error_info}")
                raise e
    '''
    def get_session(self):
        #login = self.read_yaml(r'.\yaml_test_api\buyer_login.yaml',r'test_login')
        login = self.read_yaml(r'D:\肖畅工作\ChuanchengProjecrs\buyer_api_order\yaml_test_api\buyer_login.yaml', r'test_login')
        logging.info(login)
        re = self.request_api(method = login['method'], api=login.get('api'),json = login['json'])
        headersession = {'app-sessionid': re['content']['result']['sessionid']}
        logging.info(re['content']['result'])
        logging.info(headersession)
        yaml_api_datas = yaml.dump(login)  # 把接口的请求数据转换成yaml格式，返回一个字符串对象
        temp_api_datas = Template(yaml_api_datas).substitute(
            headersession)  # 通过Template模板，把字典对象kwargs作为参数传入yaml_api_datas中（将sessionid与yaml_api_datas内容合并）
        new_api_dates = yaml.safe_load(temp_api_datas)
        logging.info(new_api_dates)
    '''


    def run_requests(self, yaml_path, api_name, **kwargs):
        '''
        ，用于读取yaml_api中的接口数据实现接口请求
        :param yaml_path: yaml文件路径
        :param api_name: yaml文件中的接口名称
        :param kwargs: 发起接口请求的自定义参数，即实现从外部传入参数到请求体中
        :return: 接口响应状态码，以及接口响应报文，返回一个字典类型
        '''
        try:
            dic_api_datas = BaseApi.read_yaml(yaml_path,api_name)  # 根据接口名字获取该接口的请求数据，返回一个字典对象
            yaml_api_datas = yaml.dump(dic_api_datas)  # 把接口的请求数据转换成yaml格式，返回一个字符串对象
            if kwargs:
                for k in kwargs.keys():  # 对传入参数数据类型为字符串的进行处理，防止模板匹配与yaml转换被转换成非字符串类型
                    logging.info(f'查看kwargs.keys(){kwargs.keys()}')
                    if k == 'head_token':
                        pass
                    elif isinstance(kwargs[k], str):
                        kwargs[k] = f"'{kwargs[k]}'"
                #将请求数据按照固定模板格式化
                #kwargs:{'sessionid': "'al:15200000001APP:c10a7f499971457d9ec01fd07e05b5ac'"}
                temp_api_datas = Template(yaml_api_datas).substitute(
                    kwargs)  # 通过Template模板，把字典对象kwargs作为参数传入yaml_api_datas中（将sessionid与yaml_api_datas内容合并）
                # 将格式化好的模板数据在转成字典类型
                api_datas = yaml.safe_load(temp_api_datas)  # 把匹配到参数的yaml格式字符串对象再次通过yaml加载的方式转换成一个字典对象

            else:
                api_datas = yaml.safe_load(yaml_api_datas)
            print(f"api_datas:{api_datas}")
            logging.info(
                f"读取YAML文件::{yaml_path}::请求的接口名称::{api_name}::传入接口参数(sessionid)::{kwargs}::接口请求参数api_datas::{api_datas}")
            logging.info(api_datas['headers'])
            response = self.request_api(method=api_datas['method'], api=api_datas['api'],
                                        headers=api_datas['headers'],
                                        params=api_datas['params'], data=api_datas['data'],
                                        json=api_datas['json'])
            logging.info(f"接口::{api_datas['api']}::响应数据为::{response}")
            return response
        except Exception as e:
            error_info = traceback.format_exc()
            logging.error(f"读取YAML文件:{yaml_path}，并发起接口请求过程中出错:{e}::错误详情:{error_info}")



    #读取yaml文件，以字典形式返回对应信息
    @staticmethod
    def read_yaml(yaml_path, title):
        file = os.path.dirname(os.path.dirname(__file__))
        yaml_path = os.path.join(file, yaml_path[2:])
        logging.info(f'yaml_path:{yaml_path},,,,{title}')
        try:
            with open(yaml_path, "r", encoding="UTF-8") as f:
                logging.info(f'yaml_path:{yaml_path},,,,{title}')
                yaml_datas = yaml.safe_load(f)  # 获取整个config.yaml全部数据，返回一个字典对象
                dic_api_datas = yaml_datas[f'{title}']  # title：config.yaml中get_case部分，根据接口名字获取该接口的请求数据，返回一个字典对象
            return dic_api_datas
        except Exception as e:
            error_info = traceback.format_exc()     #traceback.format_exc()返回详细错误信息
            logging.error(f"读取YAML文件:{yaml_path}出错:{e}::错误详情:{error_info}")

    @staticmethod
    def json_res(res, exc):
        return jsonpath.jsonpath(res, exc)

    @staticmethod
    def assert_res(res, exc):
        logging.info(exc.keys())
        for exc_key in exc.keys():
            act_value = None
            try:
                #json_res方法使用jsonpath.jsonpath()提取message
                act_value = BaseApi.json_res(res, f'$..{exc_key}')[0]
                logging.info(f"测试用例中获取到接口的断言实际值为:: 【{exc_key}:{act_value}】")
                assert act_value == exc[exc_key]
                logging.info(
                    f'测试用例通过::接口实际响应值act_value为：【{exc_key}:{act_value}】,预期为：【{exc_key}:{exc[exc_key]}】')
            except AssertionError as e:
                logging.info(
                    f'************测试用例执行失败::接口实际响应值act_value为：【{exc_key}:{act_value}】,预期为：【{exc_key}:{exc[exc_key]}】************')
                raise e

    @classmethod
    def get_path(cls, relative_path):
        '''
        文件的路径拼接，返回一个绝对路径
        :param relative_path: 文件的相对路径
        :return: 文件的绝对路径
        '''
        file_path = os.path.abspath(__file__)
        dir_path = os.path.split(file_path)[0]
        far_path = os.path.dirname(dir_path)
        path = far_path + relative_path
        return path


    def get_api_depend_dic(self, path, test_api):
        '''
        根据被测api接口，遍历所有关联接口，返回一个字典类型的关联结构图(树状结构）
        例：return::depend_api_dic -> {test_api:{api1:{api3:{api5：{},api6：{}},api4：{}},api2：{}}}
                    即 test_api 同时依赖 api1, api2
                        api1 依赖 api3, api4
                            api3 依赖 api5, api6
                            api4 无上游依赖
                        api2 无上游依赖
                    api_path_dic -> {test_api:path, api1:path1, api2:path2, api3:path3 ... aip6:path6}
                    api_depend_keys -> {test_api:{api1:[key1,key2],api2:[key3,key4}}
        '''
        depend_api_dic = {}
        depend_api_dic[test_api] = {}  # {test_api:{}}
        api_path_dic = {}
        api_path_dic[test_api] = path  # {test_api:path}
        api_depend_keys = {}
        def get_depend_dic(yaml_path, api, last_depend_dic=None,):
            # 测试api，此时层层传递过来的api传参时用例中的case名称
            # 判断yaml中api的depend依赖
            if last_depend_dic is None:
                last_depend_dic = depend_api_dic[test_api]
            else:
                pass
            dic_api_datas = BaseApi.read_yaml(yaml_path, api)  # 调用read_yaml读取接口的yaml数据返回一个字典
            '''
            例：yaml_path=‘.\yaml_test_api\buyer_login.yaml’，api='test_login',
            dic_api_datas = BaseApi.read_yaml(yaml_path, api)返回
            {api: '/api_v2/provider-app/paLogin/login',method: 'post'......depend: []}
            '''
            depend = dic_api_datas['depend']
            api_depend_keys[api] = {}
            if depend:  # depend -> [{'api':[path, api_name], 'keys':[xxx]},{'api':[xxx], 'keys':[xxx]}]
                logging.info(f'depend::{depend}')
                for d_api in depend:  # d_api -> {'api':[path, api_name], 'keys':[xxx]}
                    #例：api_depend_keys={'test_OrderQueue':{'test_login':['sessionid']}}
                    logging.info(f'd_api::{d_api}')
                    api_depend_keys[api][d_api['api'][1]] = d_api['keys']
                    last_depend_dic[d_api['api'][1]] = {}  # {first_api:{api1:{}, api2:{}}}
                    api_path_dic[d_api['api'][1]] = d_api['api'][0]
                    get_depend_dic(yaml_path=d_api['api'][0], api=d_api['api'][1],
                                   last_depend_dic=last_depend_dic[d_api['api'][1]])
                #logging.info(f'api_depend_keys：{api_depend_keys}   last_depend_dic{last_depend_dic}   api_path_dic{api_path_dic}')
            else:
                pass
        get_depend_dic(path, test_api)
        return depend_api_dic, api_path_dic, api_depend_keys

    def key_dic_list(self, get_api_depend_dic, api_depend_list=None):
        '''
        根据树状接口关联图get_api_depend_dic, 返回接口树状关联平铺列表api_depend_list
        '''
        if api_depend_list is None:
            api_depend_list = []
        api_depend_list.append(get_api_depend_dic)
        for k, v in get_api_depend_dic.items():
            self.key_dic_list(get_api_depend_dic[k],api_depend_list)
        return api_depend_list[::-1]

    def get_far_api(self, api_depend_list, api_name):
        '''
        根据传入的key(api_name)从树状关联平铺列表api_depend_list中获取该接口的下游接口，
        '''
        for dic in api_depend_list:
            for k_name, dic_value in dic.items():
                if dic_value:
                    for v_name in dic_value.keys():
                        if v_name == api_name:
                            return k_name

    def get_top_res_dic(self,path, test_api):
        #({'test_login': {}}, {'test_login': '.\\yaml_test_api\\buyer_login.yaml'}, {'test_login': {}})
        api_dic, api_path, api_depend_keys = self.get_api_depend_dic(path, test_api)
        logging.info(f"测试接口依赖树为：{api_dic}")
        api_depend_list = self.key_dic_list(api_dic)

        def top_res_dic(api_dic_par=None, res=None):
            '''
            根据树状接口关联图，获取顶端上游无依赖接口的响应存入res字典top_res_dic, 以及接口树状关联平铺列表api_depend_list
            例：return:: top_res_dic() -> {'top_api1': 'res1', 'top_api2': 'res1', 'top_api3': 'res2'}
                        api_depend_list -> [{'test_api': {'api1': {'api3': {'api5': {}, 'api6': {}}, 'api4': {}}, 'api2': {}}},
                                            {'api1': {'api3': {'api5': {}, 'api6': {}}, 'api4': {}}, 'api2': {}},
                                            {'api3': {'api5': {}, 'api6': {}}, 'api4': {}},
                                            {'api5': {}, 'api6': {}}, {}, {}, {}, {}]
            '''
            if api_dic_par is None:
                api_dic_par = api_dic
            if res is None:
                res = {}
            for k, v in api_dic_par.items():
                if v:
                    top_res_dic(api_dic_par[k], res)
                else:
                    res[k] = self.run_requests(yaml_path=api_path[k], api_name=k)
            return res
        return top_res_dic(), api_depend_list, api_path, api_depend_keys


    def make_keys_requests(self, path, test_api):
        top_res_dic, api_depend_dic_list, api_path, api_depend_keys = self.get_top_res_dic(path, test_api)
        logging.info(f"top_res_dic是：{top_res_dic}")
        #kw存放sessionid
        kw = {}
        def make_requests_from_top(api_name):
            '''
            对传入的非顶端接口，从依赖接口中获取依赖参数，并构造请求参数，发起请求，并把响应结果，按照api:res的格式存入top_res_dic中
            '''
            logging.info(f"api_depend_keys[api_name]:{api_depend_keys[api_name]}")
            for api, keys in api_depend_keys[api_name].items():
                response = top_res_dic[api]
                for key in keys:
                    #response：
                    # {'status_code': 200, 'content': {'code': 200, 'message': '调用成功。', 'result': {'sessionid': 'al:15200000001APP:cb5c5dd4b0dc4c10852e134f1c778659', 'orderWrapId': None, 'status': 1, 'type': None, 'isWechat': 1, 'isCertification': 1}}}
                    value = BaseApi.json_res(response,f'$..{key}')[0] # 根据接口的依赖key从上一个依赖接口响应中匹配value
                    kw[key] = value  # 把匹配到的key-value存放到kw字典中
                    #kw:{'sessionid': 'al:15200000001APP:c2ccc11ac0c94e57b0a6630050e7e6ab'}
            result = self.run_requests(yaml_path=api_path[api_name], api_name=api_name, **kw)
            top_res_dic[api_name] = result

        def make_depend_res(api):
            logging.info(f"接口响应数据字典集top_res_dic为：{top_res_dic.keys()}")
            logging.info(f"从top_res_dic获取到接口名api为{api}")
            far_api_name = self.get_far_api(api_depend_dic_list, api)
            logging.info(f"下游接口名far_api_name为{far_api_name}")
            if far_api_name:
                if top_res_dic.get(far_api_name):
                    pass
                else:
                    make_requests_from_top(far_api_name)
                    make_depend_res(far_api_name)

        top_depend_api_list = list(top_res_dic.keys())
        for api in top_depend_api_list:
            make_depend_res(api)
        logging.info(f"所有接口响应集top_res_dic为：{top_res_dic}")
        return top_res_dic.get(test_api)
