from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm,EditTechnicianEventForm
from django.contrib.auth.decorators import login_required
from .models import Customer ,Timeline, Order, Unit, TechnicianEvent,Document, GalleryImage
from django.shortcuts import render, get_object_or_404,redirect
from .forms import TimelineForm, OrderForm, UnitForm
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Case, When, Value, IntegerField
import boto3
from django.conf import settings
from django.core.files.storage import default_storage

# Create your views here.

def generate_signed_url(key, expires_in=3600):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    )
    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': key},
        ExpiresIn=expires_in
    )



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
    timelines = customer.timeline.all()[::-1]
    orders = customer.orders.filter(confirmed=True)
    base_prefix = f'documents/{customer.unique_code}/'
    prefix = request.GET.get('prefix', base_prefix)
    
    bucket_name = 'swsc'
    root_folder = 'documents'  # Start browsing from the documents folder

    # Listing files and folders in the root_folder
    contents = default_storage.listdir(root_folder)
    files = [file for file in contents[1] if file.startswith(root_folder)]  # Filter files to start with documents
    folders = [folder for folder in contents[0] if folder.startswith(root_folder)]  # Filter folders to start with documents


    wasabi_gallery_images = customer.wasabi_gallery.all().order_by('uploaded_at')
    grouped_images = {}
    
    for image in wasabi_gallery_images:
        image.signed_url = generate_signed_url(image.image.name)
        upload_date = image.uploaded_at.date()
        if upload_date not in grouped_images:
            grouped_images[upload_date] = []
        grouped_images[upload_date].append(image)
        
    grouped_images = dict(sorted(grouped_images.items(), reverse=True))

        

    return render(request, 'main/customer.html', {
        "customer": customer, 
        "timelines": timelines, 
        "orders": orders,
        'folders': folders,
        'files': files,
        'current_prefix': prefix,
        'base_prefix': base_prefix,
        'bucket_name': bucket_name,
        'root_folder': root_folder,
        'grouped_images': grouped_images,
    })



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
    if order.confirmed:
        return redirect('order_already_placed_error')
    
    
    if request.method == 'POST':
        unit_form = UnitForm(request.POST)
        if unit_form.is_valid():
            unit = unit_form.save(commit=False)
            unit.order = order
            unit.unit_number = unit_number
            unit.save()
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


@login_required
def order_info(request, unique_code, po_number):
    customer = get_object_or_404(Customer, unique_code=unique_code)
    order = get_object_or_404(Order, po_number=po_number, confirmed=True)
    units = order.units.all()

        
    return render(request, 'main/order_info.html', {
        'customer': customer,
        "order": order,
        "units":units
    })
    
@login_required 
def confirmation(request, unique_code, po_number):
    customer = get_object_or_404(Customer, unique_code=unique_code)
    order = get_object_or_404(Order, po_number=po_number,  confirmed=False)
    units = order.units.all()
    return render(request, 'main/order_confirmation.html', {
        'customer': customer,
        "order": order,
        "units":units
    })
    
@login_required 
def place_order(request, unique_code, po_number):
    customer = get_object_or_404(Customer, unique_code=unique_code)
    order = get_object_or_404(Order, po_number=po_number)
    order.confirmed = True
    order.save()
    return redirect('orderinfo', unique_code=unique_code, po_number=po_number)

@login_required 
def order_already_placed_error(request):
    return render(request,"errors/orderplaced.html")



@login_required
def calendar_index(request):
    return render(request, "calendar/index.html")
@login_required
def technician_calendar(request):
    a=0
    return render(request, 'calendar/technician_calendar.html',{"a":a})
@login_required
def sales_calendar(request):
    return render(request, 'calendar/sales_calendar.html')
@login_required
def delivery_calendar(request):
    return render(request, 'calendar/delivery_calendar.html')

def get_technician_events(request):
    STATUS_COLORS = {
        'installation': '#ffe073',  # yellow
        'warranty': '#efc192',  # orange
        'tech': '#62cade',  # blue
        'service': '#e2a361',  # red
    }
    
    eventtypes = {
        'installation': 'Installation',  # yellow
        'warranty': 'Warranty Service',  # yellow
        'tech': 'Tech Measure',  # blue
        'service': 'Service',  # red
    }
    
    c1_events = TechnicianEvent.objects.filter(crew='c1').order_by('start_time')
    c2_events = TechnicianEvent.objects.filter(crew='c2').order_by('start_time')
    c3_events = TechnicianEvent.objects.filter(crew='c3').order_by('start_time')
    other_events = TechnicianEvent.objects.exclude(crew__in=['c1', 'c2', 'c3']).order_by('start_time')

    events = list(c2_events) + list(c1_events) + list(c3_events) + list(other_events)
    
    events_data = []

    for event in events:
        color = STATUS_COLORS.get(event.visit_type.lower(), '#eeeeee')  
        if not event.appointment_status:
            color = "#eeeeee"
        crew_name = event.technician.name.username 
        opo = event.order.po_number
        cust = event.order.customer.unique_code
        cnum = event.crew[-1]

        events_data.append({
            'id': event.id,
            'address': event.address,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
            'color': color,
            'crew': crew_name,
            'order': event.order.po_number,  # assuming you have a po_number field in the Order model
            'visit_type': eventtypes[event.visit_type],    # to get the human-readable name of status
            'confirmed': event.confirmed,
            "status":event.appointment_status,
            'crew_label': event.crew,
            'customer':cust,
            'opo':opo,
            'cnum':cnum
        })

    return JsonResponse(events_data, safe=False)


def delete_technician_event(request, event_id):
    event = get_object_or_404(TechnicianEvent, id=event_id)
    print(event)
    if request.method == "POST":
        event.delete()
        return redirect(request.META.get('HTTP_REFERER', reverse('index'))) 

    return redirect(request.META.get('HTTP_REFERER', reverse('index'))) 



def update_technician_event(request, event_id):
    a=1
    event = get_object_or_404(TechnicianEvent, id=event_id)
    if request.method == 'POST':
        form = EditTechnicianEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect(reverse('technician_calendar'))
    else:
        form = EditTechnicianEventForm(instance=event)
    return render(request, 'calendar/technician_calendar.html', {'form': form, 'event_id': event_id, "a":a,"event":event})


def document_list(request):
    documents = Document.objects.all()
    return render(request, 'storage/document_list.html', {'documents': documents})

def gallery(request):
    images = GalleryImage.objects.all()
    for image in images:
        image.signed_url = generate_signed_url(image.image.name)
    return render(request, 'storage/gallery.html', {'images': images})


def file_browser(request):
    bucket_name = 'swsc'
    root_folder = 'documents'  # Start browsing from the root

    # Initial listing of files and folders in the root folder
    contents = default_storage.listdir(root_folder)
    files = contents[1]  # list of files
    folders = contents[0]  # list of folders

    return render(request, 'storage/file_browser.html', {
        'bucket_name': bucket_name,
        'root_folder': root_folder,
        'files': files,
        'folders': folders,
    })

def folder_contents(request):
    folder_path = request.GET.get('folder_path', '')

    # List files and folders in the specified folder_path
    contents = default_storage.listdir(folder_path)
    files = contents[1]
    print(contents)
    folders = contents[0]

    data = {
        'files': files,
        'folders': folders,
    }
    return JsonResponse(data)