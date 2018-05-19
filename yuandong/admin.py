from django.contrib import admin

from yuandong.models import YuanDongUser, YuanDongOrder,YuanDongCar


class YuanDongUserAdmin(admin.ModelAdmin):
    fields = ['key', 'nickname', 'mobile', 'IDcard', 'owner_property', 'address', 'create_time']
    search_fields = ["nickname", "key"]
    list_display = ['nickname', 'mobile', 'IDcard', 'userpush', 'carpush']

class YuanDongCarAdmin(admin.ModelAdmin):
    list_display = ['key', 'engine_sn', 'vin_number', 'plate_number', "push", "error"]
    search_fields = ["key", "nickname", "vin_number"]
    list_filter = ["push", "error"]

class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_id", "nickname", "vin_number", "money", "push", "error"]
    search_fields = ["nickname", "order_id"]
    list_filter = ["push", "error"]


admin.site.register(YuanDongUser, YuanDongUserAdmin)
admin.site.register(YuanDongCar, YuanDongCarAdmin)
admin.site.register(YuanDongOrder, OrderAdmin)
