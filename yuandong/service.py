  #！ -*- coding: utf-8 -*-
import datetime,time
import requests
from lxml import etree
import logging
from django.core.exceptions import ObjectDoesNotExist
from yuandong.models import YuanDongOrder, YuanDongUser, YuanDongCar, Aleady


logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(asctime)s %(funcName)s [line:%(lineno)d] %(levelname)-8s: %(message)s')
file_handler = logging.FileHandler("log/yuandong.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class YuanDong(object):

	def __init__(self):
		# self.proxy = "http://proxy:abc10086@cp.test.dealergood.com:6995"
		self.user_url = "http://172.17.28.10:8088/auto/customerlistAction.do"
		self.use_car_url = "http://172.17.28.10:8088/auto/vehiclelistAction.do"
		self.login_url = 'http://172.17.28.10:8088/auto/loginAction.do;jsessionid=D2BA3B687289852E41D62825A52F16FA'
		self.order_url = 'http://172.17.28.10:8088/auto/ms_svbilllistAction.do'
		self.userCarData = {
			"event": "query_all",
			"key": "null",
			"queryname": "vehicle",
			"tmpdf": "0",
			"sortField": "",
			"sortType": "",
			"formname": "vehiclelist",
			"forchoose": "",
			"currentfocusfield": "fullfObject.fvalue",
			"tmpId": "0",
			"tepName": "",
			"tepDesc": "",
			"fullfObject.fseq": "00",
			"fullfObject.ftype": "like",
			"fullfObject.fvalue": "",

			"filterObjectList[0].fseq": "00",
			"filterObjectList[0].ftype": "like",
			"filterObjectList[0].fvalue": "",

			"filterObjectList[1].fseq": "00",
			"filterObjectList[1].ftype": "like",
			"filterObjectList[1].fvalue": "",

			"filterObjectList[2].fseq": "00",
			"filterObjectList[2].ftype": "",
			"filterObjectList[2].fvalue": "",

			"filterObjectList[3].fseq": "00date",
			"filterObjectList[3].ftype": "=",
			"filterObjectList[3].fvalue": "",  # 要填值  当天

			"filterObjectList[4].fseq": "00loyalty",
			"filterObjectList[4].ftype": "=",
			"filterObjectList[4].fvalue": "",

			"filterObjectList[5].fseq": "00",
			"filterObjectList[5].ftype": "like",
			"filterObjectList[5].fvalue": "",

			"filterObjectList[6].fseq": "00",
			"filterObjectList[6].ftype": "like",
			"filterObjectList[6].fvalue": "",

			"filterObjectList[7].ftype": "=",
			"filterObjectList[7].fvalue": "",

			"filterObjectList[8].ftype": "<",
			"filterObjectList[8].fvalue": "9",

			"filterObjectList[9].ftype": "=",
			"filterObjectList[9].fvalue": "",

			"nowPage": "1",  # 第几页
			"pagerow": "20"  # 每页多少个

		}
		self.userData = {
			"event": "query_all",
			"key": "null",
			"queryname": "customer",
			"tmpdf": "0",
			"sortField": "",
			"sortType": "",
			"formname": "customerlist",
			"forchoose": "",
			"currentfocusfield": "fullfObject.fvalue",
			"tmpId": "0",
			"tepName": "",
			"tepDesc": "",
			"fullfObject.fseq": "00",
			"fullfObject.ftype": "like",
			"fullfObject.fvalue": "",

			"filterObjectList[0].fseq": "00",
			"filterObjectList[0].ftype": "like",
			"filterObjectList[0].fvalue": "",

			"filterObjectList[1].fseq": "00",
			"filterObjectList[1].ftype": "like",
			"filterObjectList[1].fvalue": "",

			"filterObjectList[2].fseq": "00area",
			"filterObjectList[2].ftype": "=",
			"filterObjectList[2].fvalue": "",

			"filterObjectList[3].fseq": "00date",
			"filterObjectList[3].ftype": "like",
			"filterObjectList[3].fvalue": "",  # 要填值  查询日期


			"filterObjectList[4].ftype": "=",
			"filterObjectList[4].fvalue": "0",


			"filterObjectList[5].ftype": "=",
			"filterObjectList[5].fvalue": "",

			"filterObjectList[6].fseq": "00user",
			"filterObjectList[6].ftype": "=",
			"filterObjectList[6].fvalue": "",

			"filterObjectList[8].fseq": "00dept",
			"filterObjectList[8].ftype": "=",
			"filterObjectList[8].fvalue": "",

			"filterObjectList[9].ftype": "=",
			"filterObjectList[9].fvalue": "",

			"nowPage": "1",  # 第几页
			"pagerow": "20"  # 每页多少个

		}
		self.orderData = {
			"event": "query_all",
			"key": "null",
			"queryname": "ms_svbill",
			"tmpdf": "0",
			"sortField": "",
			"sortType": "",
			"formname": "ms_svbilllist",
			"forchoose": "",
			"currentfocusfield": "fullfObject.fvalue",
			"tmpId": "0",
			"tepName": "",
			"tepDesc": "",
			"fullfObject.fseq": "00vehicle",
			"fullfObject.ftype": "like",
			"fullfObject.fvalue": "",

			"filterObjectList[0].fseq": "00",
			"filterObjectList[0].ftype": "like",
			"filterObjectList[0].fvalue": "",

			"filterObjectList[1].fseq": "00",
			"filterObjectList[1].ftype": "like",
			"filterObjectList[1].fvalue": "",

			"filterObjectList[2].fseq": "00sv_type",
			"filterObjectList[2].ftype": "=",
			"filterObjectList[2].fvalue": "",

			"filterObjectList[3].fseq": "00customer",
			"filterObjectList[3].ftype": "like",
			"filterObjectList[3].fvalue": "",


			"filterObjectList[4].ftype": "=",
			"filterObjectList[4].fvalue": "",

			"filterObjectList[5].fseq": "00date",
			"filterObjectList[5].ftype": ">=",
			"filterObjectList[5].fvalue": "",

			"filterObjectList[6].ftype": ">=",
			"filterObjectList[6].fvalue": "0",  # 自己填写

			"filterObjectList[7].ftype": "=",
			"filterObjectList[7].fvalue": "",

			"filterObjectList[8].ftype": "",
			"filterObjectList[8].fvalue": "",


			"nowPage": "1",  # 第几页
			"pagerow": "20"  # 每页多少列

		}
		self.headers = {
			"Content-Type": "application/x-www-form-urlencoded",
			"Proxy-Connection": "keep-alive",
			"Host": "172.17.28.10:8088",
			"Accept": "text/html, */*",
			"User-Agent": "Mozilla/3.0 (compatible; Indy Library)",
			"Cookie": "JSESSIONID=DC4B5C897A83DCBD8F8E057EC9B8FDB0;firstLogin=C013;metaLoginID=metaLoginIDc013; metaLoginType=2",
		}
		# self.login_status_code = self.login()
		self.sess = requests.session()

	# 登录

	def login(self):

		self.sess = requests.session()
		req = self.sess.get(self.login_url, headers=self.headers,timeout=10)
		cookies_dict={c.name:c.value for c in self.sess.cookies}
		# cookie=Aleady.objects.
		Cookie="{0}JSESSIONID={1};metaLoginID=metaLoginIDc013; metaLoginType=2".format("JSESSIONID",cookies_dict["JSESSIONID"])
		self.headers["Cookie"]=Cookie


	def get_resp_car(self, url, queryData):
		resp_car = self.sess.post(
		    url, data=queryData, headers=self.headers, timeout=80).text
		return resp_car

	def get_resp_user(self, url, queryData):
		resp_user = self.sess.post(
		    url, data=queryData, headers=self.headers, timeout=20).text
		return resp_user

	def get_resp_order(self, url, queryData):
		resp_order = self.sess.post(
		    url, data=queryData, headers=self.headers, timeout=20).text
		return resp_order

	# 获取用户信息保存
	def parse_car_lxml(self, resp_car):
		contentTree = etree.HTML(resp_car)
		# 所有信息
		yuandong_cars = contentTree.xpath('//*[@id="tableItemList"]/tr')[:]
	
		for yuandong_car in yuandong_cars:

			plate_number = ''.join(yuandong_car.xpath('./td[1]/div/text()')).strip()
			vin_number = ''.join(yuandong_car.xpath('./td[3]/div/text()')).strip()
			nickname = ''.join(yuandong_car.xpath('./td[4]/div/text()')).strip()
			mileage = ''.join(yuandong_car.xpath('./td[11]/div/text()')).strip()
			mobile = ''.join(yuandong_car.xpath('./td[14]/div/text()')).strip()
			engine_sn = ''.join(yuandong_car.xpath('./td[8]/div/text()')).strip()
			assure_company = ''.join(yuandong_car.xpath('./td[28]/div/text()')).strip()
			key=''.join(yuandong_car.xpath('./td[5]/div/text()')).strip()
			create_time	=''.join(yuandong_car.xpath('./td[24]/div/text()')).strip()
			create_time="-".join(create_time.split('/'))
			create_time=str(create_time)
			datetime.datetime.strptime(create_time,"%Y-%m-%d")
			# print("!!!!!!!!!!!!!!")
			# print(create_time)
			# print(type(create_time))
			car=YuanDongCar(key=key,
							plate_number =plate_number,
							vin_number=vin_number,
							nickname=nickname,
							mileage=mileage,
							mobile=mobile,
							engine_sn=engine_sn,
							create_time=create_time,
							assure_company=assure_company)
		
			print('--------------------')
			print(car.__dict__)
			print("!!!!!!!!!!!!!!!!")
			try:
				car.save()
			except	Exception as e:
				print(e)
			print("###################")

		

	def parse_user_lxml(self, resp_user):
		contentTree=etree.HTML(resp_user)
		yuandong_users=contentTree.xpath('//*[@id="tableItemList"]/tr')[:]

		for user_info in yuandong_users:
			key="".join(user_info.xpath('.//td[1]/div/text()')).strip()
			nickname="".join(user_info.xpath('.//td[2]/div/text()')).strip()
			IDcard="".join(user_info.xpath('.//td[4]/div/text()')).strip()
			mobile="".join(user_info.xpath('.//td[5]/div/text()')).strip()
			subordinate_departments="".join(user_info.xpath('.//td[11]/div/text()')).strip()
			address="".join(user_info.xpath('.//td[19]/div/text()')).strip()
			create_time="".join(user_info.xpath('.//td[15]/div/text()')).strip()
			# create_time='-'.join(str(create_time).split('/'))
			if len(nickname) > 3:
				owner_property='企业'
			else:
				owner_property='个人'
			print(nickname)


			user=YuanDongUser(key=key,
								nickname=nickname,
								IDcard=IDcard,
								mobile=mobile,
								subordinate_departments=subordinate_departments,
								address=address,
								# create_time=create_time,
								owner_property=owner_property)
			print('---------------------------')
			print(user.__dict__)
			try:
				user.save()
			except Exception as e:
				print(e)


	def parse_order_lxml(self, resp_order):
		contentTree=etree.HTML(resp_order)
		yuandong_orders=contentTree.xpath('//*[@id="tableItemList"]/tr')[:]
		# //*[@id="tableItemList"]/tbody/tr[1]/td[1]
		for order in yuandong_orders:
			nickname="".join(order.xpath('.//td[11]/div/text()')).strip()
			mobile="".join(order.xpath('.//td[21]/div/text()')).strip()
			plate_number="".join(order.xpath('.//td[4]/div/text()')).strip()
			vin_number="".join(order.xpath('.//td[8]/div/text()')).strip()

			input_time="".join(order.xpath('.//td[3]/div/text()')).strip()
			input_time='-'.join(input_time.split('/'))
			order_id="".join(order.xpath('.//td[2]/div/text()')).strip()
			server_sa="".join(order.xpath('.//td[15]/div/text()')).strip()
			money="".join(order.xpath('.//td[23]/div/text()')).strip()
			repair_type="".join(order.xpath('.//td[6]/div/text()')).strip()
			print(nickname)
			print("--------------------------------")
			order_info=YuanDongOrder(
					nickname=nickname,
					mobile=mobile,
					plate_number=plate_number,
					vin_number=vin_number,
					input_time=input_time,
					order_id=order_id,
					server_sa=server_sa,
					money=money,
					repair_type=repair_type)
			try:
				order_info.save()
			except	Exception as  e:
				print(e)

	# 拿数据的
	# query_data = datetime.datetime.now().strftime("%Y/%m/%d")
	def get_user_car(self, query_date=datetime.datetime.now().strftime("%Y/%m/%d")):
		queryData=self.userCarData
		# queryData["filterObjectList[3].fvalue"] = query_date
		# 验证是否成功
		resp_car=self.get_resp_car(self.use_car_url, queryData)
		# self.parse_car_lxml(resp_car)
		try:
			self.parse_car_lxml(resp_car)
		except Exception as e:
			print(e)
	def get_user_info(self, query_date=datetime.datetime.now().strftime("%Y/%m/%d")):
		queryData=self.userData
		# queryData["filterObjectList[3].fvalue"] = query_date
		resp_user=self.get_resp_user(self.user_url, queryData)
		# self.parse_user_lxml(resp_user)
		try:
			self.parse_user_lxml(resp_user)
		except	Exception	as	e:
			print(e)


	def get_order_info(self, query_date=datetime.datetime.now().strftime("%Y/%m/%d")):
		queryData=self.orderData
		# queryData["filterObjectList[5].fvalue"]=query_date
		resp_order=self.get_resp_order(self.order_url, queryData)
		# self.parse_order_lxml(resp_order)
		try:
			self.parse_order_lxml(resp_order)
		except	Exception	as	e:
			print(e)

		# if resp_order.status_code==200:
		# 	self.parse_order_lxml(resp_order)
		# else:
		# 	try:
		# 		self.status_code=self.login()
		# 		resp_order=self.get_resp_order(self.order_url,queryData)
		# 		self.parse_order_lxml(resp_order)
		# 	except Exception as e:
		# 		raise	Exception("denglushibai")

	def test_user_car(self):
		# 获取所有数据
		for x in range(1, 1666):
			self.userCarData["nowPage"]=x
			self.get_user_car()
	def test_user(self):
		for x in range(1, 1446):
			self.userData["nowPage"]=x
			self.get_user_info()
	def test_order(self):
		for x in range(1, 17792):
			self.orderData["nowPage"]=x
			self.get_order_info()


if __name__ == '__main__':
	yd=YuanDong()
	yd.test_user_car()
	yd.test_user()
	yd.test_order()
