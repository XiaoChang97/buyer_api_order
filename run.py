import os
import traceback

import yaml
from common.send_mail import SendEmail
from common.log import Logger
from common.zip_file import zip_files

logging = Logger(__name__).get_logger()
def run_testCase():
	test_allure = "python -m pytest -vs ./test_case_temple/ -s -q --clean-alluredir --alluredir=./result/"
	logging.info(f"run_testCase::正在执行测试命令：{test_allure}")
	try:
		os.system(test_allure)
	except Exception as e:
		logging.error(f"os执行命令{test_allure}错误：{e}")
	else:
		make_report = "allure generate ./result/ -o ./allure-report/ --clean"
		try:
			logging.info(f"run_testCase::测试执行完毕，正在执行生成报告命令：{make_report}")
			os.system(make_report)
		except Exception as e:
			logging.error(f"os执行命令{make_report}错误：{e}")
		else:
			dir_path = r'./allure-report'
			zip_path = r'./report_zip/report.zip'
			zip_report = zip_files(dir_path,zip_path)
			if zip_report:
				file_name = r'common/config.yaml'
				file_path = zip_path
				content = "测试执行结束，Allure测试报告在邮件附件中，请使用Pycharm打开查看。"
				Subject = '接口场景式自动化测试报告'  # 邮件标题
				From = "肖的QQ邮箱"  # 邮件主体中发送者名称
				To = "肖的163邮箱"  # 邮件主体中接收者名称
				try:
					with open (file_name,"r",encoding="UTF-8") as f:
						config = yaml.safe_load(f)
						config_email = config["Email"][1]
						'''
					send = SendEmail(mail_host=config_email['mail_host'], mail_user=config_email['mail_user'], mail_pass=config_email['mail_pass'],
								 sender=config_email['sender'], receives=config_email['receives'])
					send.make_email_by_att(content,file_path, Subject, From, To)
					logging.info(f"邮件发送成功，邮件标题：{Subject}")
					'''
				except Exception as e:
					error_inf = traceback.format_exc()
					logging.error(f"读取配置文件::{file_name}并发送邮件::失败::{e}::失败详情:{error_inf}")

if __name__ == '__main__':
	run_testCase()