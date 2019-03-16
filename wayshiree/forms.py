from django.forms import ModelForm
from django import forms
from .models import *
from dal import autocomplete
class TruckForm(ModelForm):
    OPTIONS = (
        ('',''),
        ('Good','Good'),
        ('Bad','Bad'),
    )
    OPTIONS1 = (
        ('',''),
        ('available','avaiable'),
        ('Not available','Not available'),
    )
    OPTIONS2 = (
        ('',''),
        ('available','avaiable'),
        ('Not available','Not available'),
    )
    OPTIONS3 = (
        ('',''),
        ('available','avaiable'),
        ('Not available','Not available'),
    )

    condition = forms.ChoiceField(choices=OPTIONS)
    gps_tracking = forms.ChoiceField(choices=OPTIONS1)
    insurance = forms.ChoiceField(choices=OPTIONS2)
    good_conduct = forms.ChoiceField(choices=OPTIONS3)

    class Meta:
        model = Truck
        fields = ['truck_number','condition','insurance','gps_tracking','owner_name','id_number','telephone_number','driver_name','driver_id_number','driver_phone_number','driving_license','good_conduct']
class OrderForm(ModelForm):

    OPTIONS = (
        ('', ''),
        ('35000', '35000'),
        ('33000', '33000'),
        ('32000', '32000'),
    )
    OPTIONS2 = (
        ('Reported to depot', 'Reported to depot'),
        ('In que', 'In que'),
        ('Loaded', 'Loaded'),
        ('Released', 'Released'),
        ('Received', 'Received'),


    )
    OPTIONS3 = (
        ('',''),
        ('PMS','PMS'),
        ('AGO','AGO'),
    )

    # truck = forms.ModelChoiceField(
    #     queryset=Truck.objects.all(),
    #     widget=autocomplete.ModelSelect2(url='truck-autocomplete')
    # )
    product = forms.ChoiceField(required=True, choices=OPTIONS3)
    order_status = forms.TypedChoiceField(required=False, choices=OPTIONS2, widget=forms.RadioSelect)
    volume = forms.ChoiceField(required=False, choices=OPTIONS)
    class Meta:
        model = Order
        fields = ['truck','date','product','depot','volume','volume_delivered','order_status','loaded_date']


class LoadingForm(ModelForm):
    OPTIONS = (
        ('',''),
        ('PMS','PMS'),
        ('AGO','AGO'),
    )
    product = forms.ChoiceField(required=True, choices=OPTIONS)
    class Meta:
        model = LoadingDashboard
        fields = ['product',  'expect_quantity' ]
class DeliveryForm(ModelForm):
    OPTIONS = (
        ('',''),
        ('PMS','PMS'),
        ('AGO','AGO'),
    )

    truck = forms.ModelChoiceField(
        queryset=Truck.objects.all(),
        widget=autocomplete.ModelSelect2(url='truck-autocomplete')
    )
    products = forms.ChoiceField(required=True, choices=OPTIONS)
    class Meta:
        model = Delivery
        fields = ['unique_number', 'truck','date_loaded', 'date_off_loaded', 'received_date', 'pic_slip_number',     'products', 'expected_quantity_to_deliver', 'recieved_quantity']
