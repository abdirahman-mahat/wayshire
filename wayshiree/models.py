from django.db import models
from django.contrib.auth.models import User
import datetime as dt

# Create your models here.

class Truck (models.Model):
    truck_number = models.CharField(max_length=200);
    condition = models.CharField(max_length=20);
    insurance = models.CharField(max_length=20);
    gps_tracking = models.CharField(max_length=20);
    owner_name = models.CharField(max_length=20);
    id_number = models.CharField(max_length=20);
    telephone_number=models.CharField(max_length=20);
    driver_name=models.CharField(max_length=30, default=None);
    driver_id_number=models.CharField(max_length=30, default=None);
    driver_phone_number=models.CharField(max_length=30, default=None);
    driving_license=models.CharField(max_length=20);
    good_conduct=models.CharField(max_length=30);
    def __str__(self):
        truck_number = self.truck_number
        return truck_number

class Order(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='relation_truck',default=None)
    date= models.DateField()
    product=models.CharField(max_length=30)
    depot = models.CharField(max_length=10)
    volume = models.CharField(max_length=30, blank=True)
    volume_delivered = models.CharField(max_length=30, blank=True)
    order_status = models.CharField(max_length=50, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)
    loaded_date = models.DateField(default=None, blank=True)
    @classmethod
    def todays_orders(cls):
        today = dt.date.today()
        orders = cls.objects.filter(pub_date__date = today)
        return orders

    def __str__(self):
        truck = self.truck
        return str(truck)


class LoadingDashboard(models.Model):
    product = models.CharField(max_length=3)
    loading_average = models.IntegerField(null=True)
    expect_quantity = models.IntegerField()
    loaded_quantity = models.IntegerField(null=True)
    remaining_quantity = models.IntegerField(null=True)
    total_trucks = models.IntegerField(null=True)
    loaded_trucks=models.IntegerField(null=True)
    remaining_trucks = models.IntegerField(null=True)
    def __str__(self):
        product = self.product
        return str(product)
class Delivery(models.Model):
    unique_number = models.CharField(default=None, max_length=30)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='relation_delivery',default=None)
    date_loaded = models.DateField()
    date_off_loaded = models.DateField()
    received_date = models.DateField(blank=True, null=True)
    pic_slip_number = models.IntegerField()
    products = models.CharField(max_length=3)
    expected_quantity_to_deliver = models.IntegerField()
    recieved_quantity = models.IntegerField()
    shortage = models.IntegerField(null=True)

    # class Meta:
    #     verbose_name = "deliverie"
    def __str__(self):
        truck = self.truck
        return str(truck)
