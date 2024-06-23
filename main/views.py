from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Customer ,Timeline, Order, Unit
from django.shortcuts import render, get_object_or_404,redirect
from .forms import TimelineForm, OrderForm, UnitForm
from django.urls import reverse
# Create your views here.

@login_required
def index(request):
    
    user = request.user
    groups = user.groups.all()
    grouplist = []
    for i in groups:
        grouplist.append(i.name)
    
    return render(request, 'main/index.html', {'grouplist': grouplist})


def timeline_create(request, unique_code):
    customer = get_object_or_404(Customer, unique_code=unique_code)
    if request.method == 'POST':
        form = TimelineForm(request.POST)
        if form.is_valid():
            timeline = form.save(commit=False)
            timeline.customer = customer
            timeline.user = request.user
            timeline.save()
            return redirect('customer', unique_code=unique_code)
    else:
        form = TimelineForm()
    return render(request, 'main/timeline_form.html', {'form': form})



@login_required
def customer(request, unique_code):
    customer = get_object_or_404(Customer, unique_code=unique_code)
    timelines = customer.timeline.all()
    return render(request, 'main/customer.html', {"customer":customer, "timelines":timelines})


# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('index')  
#     else:
#         form = UserCreationForm()
#     return render(request, 'main/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def order(request, unique_code):
    customer = get_object_or_404(Customer, unique_code=unique_code)
    
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.customer = customer
            order.save()
            # Redirect to a success page or another view
            return redirect('unit', unique_code=unique_code, po_number=order.po_number) 
        else:
            print("INVALID")
    else:
        order_form = OrderForm()
    
    return render(request, 'main/order_entry.html', {
        'oform': order_form,
        'customer': customer,
    })

@login_required
def unit(request, unique_code, po_number):
    customer = get_object_or_404(Customer, unique_code=unique_code)
    order = get_object_or_404(Order, po_number=po_number)
    unit_number = len(order.units.all()) + 1
    
    
    
    if request.method == 'POST':
        unit_form = UnitForm(request.POST)
        if unit_form.is_valid():
            unit = unit_form.save(commit=False)
            unit.order = order
            unit.save()
            return redirect('customer', unique_code=unique_code)
        else:
            print("INVALID")
            print(unit_form.errors) 
    else:
        unit_form = UnitForm()
    
    return render(request, "main/unit.html", {
        "form": unit_form,
        'customer': customer,
        "order": order,
        "unit_number": unit_number,
    })


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Timeline, id=event_id)
    
    if request.method == "POST":
        event.delete()
        return redirect(request.META.get('HTTP_REFERER', reverse('index'))) 

    return redirect(request.META.get('HTTP_REFERER', reverse('index'))) 