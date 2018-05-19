# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import django.utils.timezone as timezone


class YuanDongUser(models.Model):
    key = models.CharField(max_length=100, unique=True, verbose_name='用户编号')
    nickname = models.CharField(max_length=200, verbose_name='用户名')
    owner_property = models.CharField(
        max_length=20, default="个人", verbose_name='用户属性')
    subordinate_departments = models.CharField(
        max_length=200, blank=True, verbose_name='隶属部门')
    mobile = models.CharField(max_length=100, blank=True, verbose_name='手机')
    IDcard = models.CharField(max_length=100, blank=True, verbose_name='身份证')
    address = models.CharField(max_length=100, blank=True, verbose_name='地址')
    update = models.BooleanField(default=False, verbose_name='更新推送')
    create_time = models.DateTimeField(
        null=True, blank=True, verbose_name='建档日期')
    update_time = models.DateTimeField(
        null=True, default=timezone.now, verbose_name='更新时间')
    userpush = models.BooleanField(default=False, verbose_name='用户推送状态')
    carpush = models.BooleanField(default=False, verbose_name='车辆推送状态')
    usererror = models.BooleanField(default=False, verbose_name='用户推送结果')
    carerror = models.BooleanField(default=False, verbose_name='车辆推送结果')


class YuanDongCar(models.Model):
    key = models.CharField(max_length=100, unique=True,
                           blank=True, default="11111111", verbose_name='用户编号')
    nickname = models.CharField(max_length=200, verbose_name='用户名')
    vin_number = models.CharField(max_length=100, verbose_name='VIN')
    mobile = models.CharField(max_length=100, null=True, verbose_name='手机')
    plate_number = models.CharField(
        max_length=100, null=True, verbose_name='车牌号')
    engine_sn = models.CharField(max_length=40, null=True, verbose_name='发动机号')
    mileage = models.CharField(
        max_length=100, default='0', verbose_name='出厂公里')
    create_time = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='建档日期')
    assure_company = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='保险公司')
    update = models.BooleanField(default=False, verbose_name='更新推送')
    update_time = models.DateTimeField(
        null=True, default=timezone.now, verbose_name='更新时间')
    push = models.BooleanField(default=False, verbose_name='车辆推送状态')
    error = models.BooleanField(default=False, verbose_name='车辆推送结果')


class YuanDongOrder(models.Model):
    key = models.CharField(max_length=100, blank=True, verbose_name='用户编号')
    shop_name = models.CharField(max_length=100, default="上海一汽丰田元东")
    server_sa = models.CharField(
        max_length=100, blank=True, verbose_name='服务专员')
    order_id = models.CharField(
        max_length=100, blank=True, verbose_name='订单编号')
    input_time = models.CharField(
        max_length=100, blank=True, verbose_name='订单日期')
    nickname = models.CharField(
        max_length=100, blank=True, verbose_name='客户姓名')
    mobile = models.CharField(max_length=100, blank=True, verbose_name='客户手机号')
    plate_number = models.CharField(
        max_length=100, blank=True, verbose_name='车牌号')
    vin_number = models.CharField(
        max_length=100, blank=True, verbose_name='vin')

    money = models.CharField(max_length=30, blank=True, verbose_name='费用')
    repair_type = models.CharField(
        max_length=30, blank=True, verbose_name='维修类型')
    item = models.TextField(blank=True, verbose_name='维修项目')
    #material = models.TextField(blank=True, verbose_name='维修零件')
    #mileage = models.CharField(max_length=100, default='0', verbose_name='出厂公里')
    push = models.BooleanField(default=False, verbose_name='推送状态')
    error = models.BooleanField(default=False, verbose_name='推送结果')

    def __str__(self):
        return self.order_id

    class Meta:
        verbose_name = '维修工单'
        verbose_name_plural = '维修工单'


# class Employee(models.Model):
#     employee_no = models.CharField(max_length=100, blank=True, verbose_name='服务专员编号')
#     employee_name = models.CharField(max_length=100, blank=True, verbose_name='服务专员')

class Aleady(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
