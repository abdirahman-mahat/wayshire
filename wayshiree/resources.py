from import_export import resources
from .models import *
class TruckResource(resources.ModelResource):
    class Meta:
        model = Truck
        fields = ('truck_number','condition','insurance','gps_tracking','owner_name','id_number','telephone_number','driver_name', 'driver_id_number','driver_phone_number','driving_license','good_conduct')
class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('truck__truck_number','date','product','depot','truck__driver_name','truck__driver_id_number', 'truck__driver_phone_number')
