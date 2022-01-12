import os
import zipfile
from common.log import Logger

logging = Logger(__name__).get_logger()
def zip_files(dir_path,zip_path):
	'''
	:param dir_path: 需要压缩的文件夹地址  例：'D:\Buyer_test_code\apipotest_jcmall\report'
	:param zip_path: 压缩后的文件存在地址+压缩文件名  例：'D:\Buyer_test_code\apipotest_jcmall\report_zip\report.zip'
	:return: 0  压缩失败  1 压缩成功
	'''
	try:
		with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as f:
			for dirpath, dirnames, filenames in os.walk(dir_path):
				fpath = dirpath.replace(dir_path, '')
				fpath = fpath and fpath + os.sep or ''
				for filename in filenames:
					f.write(os.path.join(dirpath, filename), fpath+filename)
			logging.info(f"文件：{dir_path} 压缩成功")
	except Exception as e:
		logging.error(f"文件：{dir_path} 压缩失败，错误：{e}")
		return 0
	else:
		return 1


if __name__ == '__main__':
	dir_path = r'../report'
	zip_path = r'../report_zip/report.zip'
	z = zip_files(dir_path,zip_path)

