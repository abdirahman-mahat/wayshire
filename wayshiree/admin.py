from __future__ import unicode_literals
import csv
from django.contrib import admin
from django import forms
from .forms import *
# Register your models here.
# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.

admin.site.site_header="WAYSHIRE Admin"
admin.site.site_title="WAYSHIRE Admin Portal"
admin.site.index_title="Welcome to WAYSHIRE Data Entry and Data Modifications"

class TruckAdmin(ImportExportModelAdmin):
    fields = ('truck_number','condition','insurance','gps_tracking','owner_name','id_number','telephone_number','driver_name', 'driver_id_number','driver_phone_number','driving_license','good_conduct')
    form = TruckForm
    search_fields = ['truck_number']
admin.site.register(Truck, TruckAdmin)

class OrderAdmin( ImportExportModelAdmin):
    model = Order
    fields = ('truck','date','product','depot')
    form = OrderForm
    search_fields = ['truck__truck_number']
    autocomplete_fields = ['truck']



admin.site.register(Order, OrderAdmin)

class LoadingAdmin(admin.ModelAdmin):
    model = LoadingDashboard
    fields = ('product','expect_quantity')
    form = LoadingForm
admin.site.register(LoadingDashboard, LoadingAdmin)
class DeliveryAdmin(ImportExportModelAdmin):
    model = Delivery
    fields = ('unique_number', 'truck','date_loaded', 'date_off_loaded',  'pic_slip_number',     'products', 'expected_quantity_to_deliver', 'recieved_quantity', )
    form = DeliveryForm
    search_fields = ['truck__truck_number']

admin.site.register(Delivery, DeliveryAdmin)
