from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,FormView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from .resources import *
from tablib import Dataset
from dal import autocomplete
from django.views.generic import ListView
# from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Sum
from django.db.models import Count


def orders_today(request):
    date = dt.date.today()
    orders = Order.todays_orders()
    return render(request, 'todays-orders.html', {"date": date,"orders":orders})
class TruckAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return Truck.objects.none()
        qs = Truck.objects.all()
        if self.q:
            qs = qs.filter(truck_number__istartswith=self.q)

        return qs
def check_admin(user):
   return user.is_superuser

@login_required(login_url='/accounts/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })
@login_required(login_url='/accounts/login/')
def index(request):
    trucks = Truck.objects.all()

    return render(request, 'index.html', {'trucks': trucks})
@login_required(login_url='/accounts/login/')
def loading(request):
    loaded = Order.objects.filter(Q(order_status='Loaded') | Q(order_status='Released')| Q(order_status='Received') )[0:200]
    # loaded =   Loaded.objects.filter(order__order_status__in=['Loaded', 'Released'])
    return render(request, 'loadings.html' , {'loaded':loaded})

@login_required(login_url='/accounts/login/')
def loading_dashboard(request):
    # import pdb; pdb.set_trace()

    loaded = LoadingDashboard.objects.all()
    for math in loaded:
        volume = list(Order.objects.filter(product='PMS')
        .values_list('volume_delivered', flat=True))
        order = volume
        sum = 0
        for volume in order:
            sum = sum + int(volume)

        trucks = Order.objects.filter(product='PMS').count()
        loading = Order.objects.filter(product='PMS').filter( Q(order_status='Loaded') | Q(order_status='Released') | Q(order_status='Received')).count()

        volume_ago = list(Order.objects.filter(product='AGO')
        .values_list('volume_delivered', flat=True))
        order_ago = volume_ago
        sum_ago = 0
        for volume in order_ago:
            sum_ago = sum_ago + int(volume)

        trucks_ago = Order.objects.filter(product='AGO').count()
        loading_ago = Order.objects.filter(product='AGO').filter(Q(order_status='Loaded') | Q(order_status='Released') | Q(order_status='Received')).count()
        if math.product == 'PMS':
            math.loading_average = sum // trucks // 1000
            math.total_trucks = math.expect_quantity // math.loading_average
            math.loaded_quantity = sum // 1000
            math.remaining_quantity = math.expect_quantity - math.loaded_quantity
            math.loaded_trucks = loading
            math.remaining_trucks = math.total_trucks - math.loaded_trucks
        elif math.product == 'AGO':
            math.loading_average = sum_ago // trucks_ago // 1000
            math.total_trucks = math.expect_quantity // math.loading_average
            math.loaded_quantity = sum_ago // 1000
            math.remaining_quantity = math.expect_quantity - math.loaded_quantity
            math.loaded_trucks = loading_ago
            math.remaining_trucks = math.total_trucks - math.loaded_trucks
    return render(request, 'loadings_dashboard.html' , {'loaded': loaded})
@login_required(login_url='/accounts/login/')
def delivery(request):
    delivery = Delivery.objects.all()
    for math in delivery:
        math.shortage = math.expected_quantity_to_deliver - math.recieved_quantity
    return render(request, 'delivery.html' , {'delivery': delivery})
@login_required(login_url='/accounts/login/')
def show(request, truck_id):
    truck = Truck.objects.filter(id=truck_id)
    return render(request, 'show.html', {'truck': truck})
@login_required(login_url='/accounts/login/')
def order(request):
    orders = Order.objects.all()
    return render(request, 'order.html', {'orders':orders})
@login_required(login_url='/accounts/login/')
def edit_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.POST:
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            if form.save():
                return redirect('/order', messages.success(request, 'order was successfully updated.', 'alert-success'))
            else:
                return redirect('/order', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/order', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = OrderForm(instance=order)
        return render(request, 'edit_order.html', {'form':form})
@login_required(login_url='/accounts/login/')
def edit_delivery(request, delivery_id):
    delivery = Delivery.objects.get(id=delivery_id)
    if request.POST:
        form = DeliveryForm(request.POST, instance=delivery)
        if form.is_valid():
            if form.save():
                return redirect('/delivery', messages.success(request, 'delivery was successfully updated.', 'alert-success'))
            else:
                return redirect('/delivery', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/delivery', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = DeliveryForm(instance=delivery)
        return render(request, 'edit_delivery.html', {'form':form})
@login_required(login_url='/accounts/login/')
def loading_status(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.POST:
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            if form.save():
                return redirect('/loading', messages.success(request, 'Loading Status was successfully updated.', 'alert-success'))
            else:
                return redirect('/loading', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/loading', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = OrderForm(instance=order)
        return render(request, 'loading_status.html', {'form':form})
@login_required(login_url='/accounts/login/')
def show_order(request, order_id):
    order = Order.objects.filter(id=order_id)
    return render(request, 'show_order.html', {'order': order})
@user_passes_test(check_admin)
def finance(request):
    return render(request, 'finance.html')

def export(request):
    truck_resource = TruckResource()
    dataset = truck_resource.export()
    response = HttpResponse(dataset.xls, content_type ='application/vnd.ms-excel')
    response['Content-Dispositon'] = 'attachment; filename="truck.xls"'
    return response
def export_order(request):
    order_resource = OrderResource()
    dataset = order_resource.export()
    response = HttpResponse(dataset.xls, content_type ='application/vnd.ms-excel')
    response['Content-Dispositon'] = 'attachment; filename="order.xls"'
    return response

def simple_upload(request):
    if request.method == 'POST':
        truck_resource = TruckResource()
        dataset = Dataset()
        new_trucks = request.FILES['myfile']

        imported_data = dataset.load(new_trucks.read())
        result = truck_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            truck_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'simple_upload.html')
