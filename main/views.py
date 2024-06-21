from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Customer ,Timeline
from django.shortcuts import render, get_object_or_404
from .forms import TimelineForm
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


def order(request):
    return render(request, "main/order_entry.html")