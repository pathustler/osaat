from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm,EditTechnicianEventForm
from django.contrib.auth.decorators import login_required
from .models import Customer ,Timeline, Order, Unit, TechnicianEvent,Document, GalleryImage, SalesEvent, DeliveryEvent
from django.shortcuts import render, get_object_or_404,redirect
from .forms import *
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
import boto3
from django.conf import settings
from django.core.files.storage import default_storage
from django.forms import modelformset_factory
from django.db import transaction


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

    # Generate signed URLs for each file
    signed_urls = {}
    for file in files:
        key = root_folder + file
        signed_urls[file] = generate_signed_url(key)

    wasabi_gallery_images = customer.wasabi_gallery.all().order_by('uploaded_at')
    grouped_images = {}
    
    for image in wasabi_gallery_images:
        print("GALLERY : ",image.image.name)
        image.signed_url = generate_signed_url(image.image.name)
        upload_date = image.uploaded_at.date()
        if upload_date not in grouped_images:
            grouped_images[upload_date] = []
        grouped_images[upload_date].append(image)
        
    grouped_images = dict(sorted(grouped_images.items(), reverse=True))
    
    
    if request.method == 'POST':
        techform = TechnicianEventForm(request.POST,unique_code=unique_code)
        salesform = SalesEventForm(request.POST,unique_code=unique_code)
        deliveryform = DeliveryEventForm(request.POST)
        job_forms_data = request.POST.getlist('jobs')
        
        job_order_ids = request.POST.getlist('job_order')
        job_titles = request.POST.getlist('job_title')

        if techform.is_valid():
            tech_event = techform.save(commit=False)
            tech_event.save()
            return redirect(reverse('technician_calendar'))

        elif salesform.is_valid():
            sales_event = salesform.save(commit=False)
            sales_event.save()
            return redirect(reverse('sales_calendar'))

        elif deliveryform.is_valid():
            delivery_event = deliveryform.save(commit=False)
            delivery_event.save()

            for order_id, title in zip(job_order_ids, job_titles):
                if order_id and title:
                    job = Job.objects.create(order_id=order_id, title=title)
                    delivery_event.jobs.add(job)

            delivery_event.save()
            return redirect(reverse('delivery_calendar'))
    else:
        techform = TechnicianEventForm(unique_code=unique_code)
        salesform = SalesEventForm(unique_code=unique_code)
        deliveryform = DeliveryEventForm()

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
        'signed_urls': signed_urls,  # Pass signed URLs to the template
        "customer": customer,
        "techform": techform,
        "salesform": salesform,
        "deliveryform": deliveryform,
        "orders": Order.objects.filter(customer__unique_code=unique_code)
    })
    
    
def folder_contents(request):
    folder_path = request.GET.get('folder_path', '')

    # List files and folders in the specified folder_path
    contents = default_storage.listdir(folder_path)
    files = contents[1]
    folders = contents[0]

    data = {
        'files': [],
        'folders':folders
    }

    for file_name in files:
        key = folder_path+"/"+file_name
        if "//" in key:
            key = key.replace("//","/")
        print("FOR VIEWER FILES : ",key)
        signed_url = generate_signed_url(key)
        data['files'].append([file_name, signed_url])

    return JsonResponse(data)


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
    a=0
    return render(request, 'calendar/sales_calendar.html')
@login_required
def delivery_calendar(request):
    a=0
    unscheduled = DeliveryEvent.objects.filter(Q(start_time__isnull=True) | Q(end_time__isnull=True))
    alljobs = dict()
    for event in unscheduled:
        alljobs[event.id] = list(event.jobs.all())
    for job in alljobs:
        print(job)
    return render(request, 'calendar/delivery_calendar.html', {"unscheduled":unscheduled, "alljobs":alljobs,"a":a})

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
        if event.crew=="unset":
            cnum= "Unset"

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



def get_sales_events(request):
    STATUS_COLORS = {
        'active': '#badbbb',  # green
        'estimate': '#eeeeee',  # gray
        'sold': '#62cade',  # blue
        'cancelled': '#e2a361',  # red
    }

    events = SalesEvent.objects.all().order_by('start_time')
    events_data = []

    for event in events:
        color = STATUS_COLORS.get(event.status, '#eeeeee')
        events_data.append({
            'id': event.id,
            'salesperson': event.salesperson.name.username,  # Assuming Crew model has a 'name' related to User model
            'order': event.order.po_number,  # Assuming Order model has a 'po_number' field
            'title': event.title,
            'main_phone': event.main_phone,
            'address': event.address,
            'appointment_notes': event.appointment_notes,
            'status': event.status,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
            'color': color,
        })

    return JsonResponse(events_data, safe=False)


def get_delivery_events(request):
    STATUS_COLORS = {
        'azloop': '#f8be4e',  # orange
        'route1': '#81c897',  # green
    }

    events = DeliveryEvent.objects.filter(Q(start_time__isnull=False) & Q(end_time__isnull=False)).order_by('start_time')
    events_data = []

    for event in events:
        color = STATUS_COLORS.get(event.route, '#888888')
        units = 0
        statuscolor = "#3ea254"
        jobs = []
        
        for i in event.jobs.all():
            orderunits = i.order.units.all()
            units +=len(orderunits)
            
            if i.status != "delivered":
                statuscolor = "#d3222a"
            jobs.append([i.title,i.status, i.order.po_number])
        group=0
        if len(event.jobs.all())>1:
            group = 1
            
        events_data.append({
            'id': event.id, 
            'jobs': jobs,  
            'units':units,
            'title': event.title,
            'main_phone': event.main_phone,
            'address': event.address,
            'special_instructions': event.special_instructions,
            'statuscolor': statuscolor,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
            'color': color,
            'group':group,
            'route':event.get_route_display(),
        })

    return JsonResponse(events_data, safe=False)



def delete_technician_event(request, event_id):
    event = get_object_or_404(TechnicianEvent, id=event_id)
    print(event)
    if request.method == "POST":
        event.delete()
        return redirect(request.META.get('HTTP_REFERER', reverse('index'))) 

    return redirect(request.META.get('HTTP_REFERER', reverse('index'))) 

def delete_sales_event(request, event_id):
    event = get_object_or_404(SalesEvent, id=event_id)
    print(event)
    if request.method == "POST":
        event.delete()
        return redirect(request.META.get('HTTP_REFERER', reverse('index'))) 

    return redirect(request.META.get('HTTP_REFERER', reverse('index'))) 

def delete_delivery_event(request, event_id):
    event = get_object_or_404(DeliveryEvent, id=event_id)
    print(event)
    if request.method == "POST":
        event.delete()
        return redirect(request.META.get('HTTP_REFERER', reverse('index'))) 

    return redirect(request.META.get('HTTP_REFERER', reverse('index'))) 


def update_technician_event(request, event_id):
    event = get_object_or_404(TechnicianEvent, id=event_id)
    if request.method == 'POST':
        form = EditTechnicianEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect(reverse('technician_calendar'))
    else:
        form = EditTechnicianEventForm(instance=event)
        form.initial['appointment_status'] = event.appointment_status
        print("Event appointment status:", event.appointment_status)  # Debug statement
        print("Form initial appointment status:", form.initial['appointment_status'])  # Debug statement
    
    return render(request, 'calendar/technician_calendar.html', {
        'form': form,
        'event_id': event_id,
        'a': 1,
        'event': event
    })
    
    
    
def update_sales_event(request, event_id):
    a=1
    event = get_object_or_404(SalesEvent, id=event_id)
    if request.method == 'POST':
        form = EditSalesEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect(reverse('sales_calendar'))
    else:
        form = EditSalesEventForm(instance=event)
    return render(request, 'calendar/sales_calendar.html', {'form': form, 'event_id': event_id, "a":a,"event":event})

def update_delivery_event(request, event_id):
    a=1
    event = get_object_or_404(DeliveryEvent, id=event_id)
    
    unscheduled = DeliveryEvent.objects.filter(Q(start_time__isnull=True) | Q(end_time__isnull=True))
    alljobs = dict()
    for event in unscheduled:
        alljobs[event.id] = list(event.jobs.all())
    for job in alljobs:
        print(job)
        
    if request.method == 'POST':
        form = EditDeliveryEventForm(request.POST, instance=event)
        jobforms = []
        for job in event.jobs.all():
            job_form = EditJobForm(request.POST, instance=job)
            jobforms.append([job.order.po_number, job_form])
        jobs_valid = all(job_form.is_valid() for _, job_form in jobforms)
        
        if form.is_valid() and jobs_valid:
            event = form.save(commit=False)
            event.route = form.cleaned_data['route']
            print(form.cleaned_data['route'])
            print(event.route)
            event.save()
            for _, job_form in jobforms:
                job_form.save()
            return redirect(reverse('delivery_calendar'))
    else:
        form = EditDeliveryEventForm(instance=event)
        jobforms = []
        for job in event.jobs.all():
            job_form = EditJobForm(instance=job)
            jobforms.append([job.order.po_number, job_form])
    
    return render(request, 'calendar/delivery_calendar.html', {'form': form, 'event_id': event_id, "event": event, "jobforms": jobforms,"a":a,"unscheduled":unscheduled, "alljobs":alljobs})


def schedule_delivery_event(request, event_id):
    a=2
    event = get_object_or_404(DeliveryEvent, id=event_id)
    
    unscheduled = DeliveryEvent.objects.filter(Q(start_time__isnull=True) | Q(end_time__isnull=True))
    alljobs = dict()
    for event in unscheduled:
        alljobs[event.id] = list(event.jobs.all())
    for job in alljobs:
        print(job)
        
    if request.method == 'POST':
        form = ScheduleDeliveryEventForm(request.POST, instance=event)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('delivery_calendar'))
    else:
        form = ScheduleDeliveryEventForm(instance=event)
    
    return render(request, 'calendar/delivery_calendar.html', {'form': form, 'event_id': event_id, "event": event,"a":a, "unscheduled":unscheduled, "alljobs":alljobs})



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



@login_required
def schedule(request, unique_code):
    customer = get_object_or_404(Customer, unique_code=unique_code)
    
    if request.method == 'POST':
        techform = TechnicianEventForm(request.POST)
        salesform = SalesEventForm(request.POST)
        deliveryform = DeliveryEventForm(request.POST)
        job_forms_data = request.POST.getlist('jobs')
        
        job_order_ids = request.POST.getlist('job_order')
        job_titles = request.POST.getlist('job_title')


        if techform.is_valid():
            tech_event = techform.save(commit=False)
            tech_event.save()
            return redirect(reverse('technician_calendar'))

        elif salesform.is_valid():
            sales_event = salesform.save(commit=False)
            sales_event.save()
            return redirect(reverse('sales_calendar'))

        elif deliveryform.is_valid():
            delivery_event = deliveryform.save(commit=False)
            delivery_event.save()

            for order_id, title in zip(job_order_ids, job_titles):
                if order_id and title:
                    job = Job.objects.create(order_id=order_id, title=title)
                    delivery_event.jobs.add(job)

            delivery_event.save()
            return redirect(reverse('delivery_calendar'))
    else:
        techform = TechnicianEventForm()
        salesform = SalesEventForm()
        deliveryform = DeliveryEventForm()
    
    return render(request, 'calendar/schedule.html', {
        "customer": customer,
        "techform": techform,
        "salesform": salesform,
        "deliveryform": deliveryform,
        "orders": Order.objects.filter(customer__unique_code=unique_code)
    })
    
    
    
def search(request):
    query = request.GET.get('q')
    customers = Customer.objects.filter(primary_contact__icontains=query)
    orders = Order.objects.filter(po_number__icontains=query)
    context = {
        'customers': customers,
        'orders': orders,
        'query': query,
        'total':len(customers)+len(orders)
    }
    return render(request, 'main/search_results.html', context)



from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction
from django.http import HttpResponseBadRequest
from .models import Customer, Order, Unit
from .forms import OrderForm, UnitForm

def order_wizard(request, unique_code):
    customer = get_object_or_404(Customer, unique_code=unique_code)

    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        # Retrieve all unit form fields as lists
        product_types = request.POST.getlist('product_type')
        widths = request.POST.getlist('width')
        drops = request.POST.getlist('drop')
        handings = request.POST.getlist('handing')
        motor_types = request.POST.getlist('motor_type')
        fabric_types = request.POST.getlist('fabric_type')
        fabric_colors = request.POST.getlist('fabric_color')
        mountings = request.POST.getlist('mounting')
        accessories = request.POST.getlist('accessory')
        remote_types = request.POST.getlist('remote_type')
        hand_braces = request.POST.getlist('hand_brace')
        hardware_colors = request.POST.getlist('hardware_color')
        box_colors = request.POST.getlist('box_color')
        cable_mounts = request.POST.getlist('cable_mount')
        cable_sizes = request.POST.getlist('cable_size')
        pile_brushes = request.POST.getlist('pile_brush')

        unit_forms_data = []

        for i in range(len(product_types)):
            unit_data = {
                'product_type': product_types[i],
                'width': widths[i],
                'drop': drops[i],
                'handing': handings[i],
                'motor_type': motor_types[i],
                'fabric_type': fabric_types[i],
                'fabric_color': fabric_colors[i],
                'mounting': mountings[i],
                'accessory': accessories[i],
                'remote_type': remote_types[i],
                'hand_brace': hand_braces[i],
                'hardware_color': hardware_colors[i],
                'box_color': box_colors[i],
                'cable_mount': cable_mounts[i],
                'cable_size': cable_sizes[i],
                'pile_brush': pile_brushes[i],
            }
            unit_forms_data.append(unit_data)

        unit_forms = [UnitForm(data) for data in unit_forms_data]

        if order_form.is_valid() and all(form.is_valid() for form in unit_forms):
            with transaction.atomic():
                order = order_form.save(commit=False)
                order.customer = customer
                order.save()

                for i, form in enumerate(unit_forms):
                    unit = form.save(commit=False)
                    unit.order = order
                    unit.unit_number = i + 1  # Assigning the unit number
                    unit.save()

            return redirect('confirmation', unique_code=unique_code, po_number=order.po_number)  # Replace with your success URL

        else:
            return render(request, 'main/order_wizard.html', {
                'customer': customer,
                'oform': order_form,
                'unit_forms': unit_forms,
            })

    else:
        order_form = OrderForm()
        unit_form = UnitForm()

    return render(request, 'main/order_wizard.html', {
        'customer': customer,
        'oform': order_form,
        'form': unit_form,
    })
    
    
    
