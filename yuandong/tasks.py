#! -*- coding: utf-8 -*-
import hashlib
import json
import datetime
import time
import requests
from yuandong.models import YuanDongUser, YuanDongCar, YuanDongOrder
from yuandong.service import YuanDong
from clientrobot.celery import app

company_id = ""
sys_name = "shop_id-yuandongDMS"
timestamp = int(time.time())
token = ""
m = '1994/01/01'
# sign


def get_md5_pwd(company_id, sys_name, token, timestamp):
    hl = hashlib.md5()
    hl.update((company_id + sys_name + token +
               str(timestamp)).encode(encoding='utf-8'))
    return hl.hexdigest()


sign = get_md5_pwd(company_id, sys_name, token, timestamp)
endUrl = "sys_name={0}&company_id={1}&sign={2}&timestamp={3}".format(
    sys_name, company_id, sign, str(timestamp))

# 查询用户当天


def yuandong_update_user_car(yuandong, d=datetime.date.today()):
    # m = '2010/01/01'
    yuandong.get_user_car()

# 查询当天用户维修记录


def yuandong_update_order(yuandong, d=datetime.date.today()):
    # m = '2010/01/01'
    yuandong.get_order_info()


def yuandong_update_user(yuandong):
    # m='2010/01/01'
    yuandong.get_user_info()
# 发给php


def yuandong_push_user():
    users = YuanDongUser.objects.filter(userpush=False, usererror=False)[:100]
    url = "http://cp.test.dealergood.com/api/member/postData?" + endUrl
    sess = 0
    user_list = []
    if len(users) != 0:
        for user in users:
            if len(user.mobile) != 11:
                user.mobile = "00000000000"
            user_list.append(
                {
                    "key": user.key,
                    # "action": 1,
                    "nickname": user.nickname,
                    "IDcard": user.IDcard,
                    "address": user.address,
                    "mobile": user.mobile,
                    "shop_id": 8245,  # 要改
                    "shop_name": "一汽车田元动",
                    # "customer_type": user.owner_property
                }
            )
        headers = {"Content-type": "application/json"}
        data = json.dumps(user_list)
        res = requests.post(url=url, headers=headers, data=data, timeout=60)
        res_json = res.json()
        print(res_json)
        error = res_json.get("error", "1")
        if error == 3:
            return
        elif error == "0":
            for user in users:
                sess += 1
                user.userpush = True
                user.save(update_fields=["userpush"])
        else:
            for user in users:
                user.usererror = True
                user.save(update_fields=["usererror"])
    print(sess)
    return len(users)


def yuandong_push_car():
    cars = YuanDongCar.objects.filter(push=False, error=False)[:100]
    url = "http://cp.test.dealergood.com/api/memberCar/postData?" + endUrl
    sess = 0
    car_list = []
    if len(cars) != 0:
        for car in cars:
            if len(car.mobile) != 11:
                car.mobile = "00000000000"
            car_list.append(
                {
                    "key": car.key,
                    "shop_id": 8245,  # 要改
                    # "action": 1,
                    "nickname": car.nickname,
                    "mobile": car.mobile,
                    "vin_number": car.vin_number,
                    "plate_number": car.plate_number,
                    "engine_sn": car.engine_sn,
                    "register_date": car.create_time
                }
            )
        headers = {"Content-type": "application/json"}
        data = json.dumps(car_list)
        res = requests.post(url=url, headers=headers, data=data, timeout=60)
        res_json = res.json()
        print(res_json)
        error = res_json.get("error", "1")
        if error == 3:
            return
        elif error == "0":
            for car in cars:
                sess += 1
                car.push = True
                car.save(update_fields=["push"])
        else:
            for car in cars:
                car.error = True
                car.save(update_fields=["error"])
    print(sess)
    return len(cars)


def yuandong_push_order():
    orders = YuanDongOrder.objects.filter(push=False, error=False)[:100]
    url = "http://cp.test.dealergood.com/api/workOrder/postData?" + endUrl
    sess = 0
    if len(orders) != 0:
        order_list = []
        for order in orders:
            order_list.append({
                "key": order.key,
                #"shop_id": 8245, 要改
                "server_sa": order.server_sa,
                "order_id": order.order_id,
                "input_time": order.input_time,
                "nickname": order.nickname,
                "mobile": order.mobile,
                "vin_number": order.vin_number,
                "plate_number": order.plate_number,

                # "mileage": order.mileage, 出厂公里
                "money": order.money,
                "item": order.item,
                "material": order.material,
                # "repair_type": order.type,
                "shop_name": "一汽车田元动"
            })
        headers = {"Content-type": "application/json"}
        data = json.dumps(order_list)
        res = requests.post(url=url, headers=headers, data=data, timeout=60)
        res_json = res.json()
        print(res_json)
        error = res_json.get("error", "1")
        if error == 3:
            return
        elif error == "0":
            for order in orders:
                sess += 1
                order.push = True
                order.save(update_fields=["push"])
        else:
            for order in orders:
                order.error = True
                order.save(update_fields=["error"])
    print(sess)
    return len(orders)


def push_all():
    users = YuanDongUser.objects.all()
    for user in users:
        user.userpush = False
        user.save(update_fields=["userpush"])
    cars = YuanDongCar.objects.all()
    for car in cars:
        car.push = False
        car.save(update_fields=["push"])
    orders = YuanDongOrder.objects.all()
    for order in orders:
        order.push = False
        order.save(update_fields=["push"])
    while True:
        l = yuandong_push_user()
        if l is None:
            time.sleep(10)
            continue
        if l == 0:
            break
    while True:
        l = yuandong_push_car()
        if l is None:
            time.sleep(10)
            continue
        if l == 0:
            break
    while True:
        l = yuandong_push_order()
        if l is None:
            time.sleep(10)
            continue
        if l == 0:
            break


@app.task(name="yuandong_task")
def yuandong_tasks():
    # 先查询 在推送
    # yuandong = YuanDong()

    yd=YuanDong()
    yd.test_user_car()
    yd.test_user()
    yd.test_order()
    # 拿到用户登录日期
    # date = datetime.date.today()

    # # 拿到用户当天数据
    # yuandong_update_user_car(yuandong, m)
    # # 查询历史数据
    # yuandong_update_order(yuandong, m)
    # yuandong_update_user(yuandong)
    # yuandong_push_user()
    # yuandong_push_car()
    # yuandong_push_order()
