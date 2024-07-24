from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import BoxCutJobForm
from main.models import Order
from .models import Box_Cut_Job
# Create your views here.


def workstation_dashboard(request):
    return render(request,"workstation/index.html")


def job_search(request, job_type):
    orders = Order.objects.filter(confirmed=True)
    label = {
        "box_cut": "Box Cut"
    }[job_type]
    
    return render(request,"workstation/job_search.html", {"job_type":job_type,"label":label})

def box_cut(request, po_number):
    order = get_object_or_404(Order.objects.filter(confirmed=True), po_number=po_number)
    unitforms = dict()
    totalunits = len(order.units.all())
    print("enters")

    if request.method == 'POST':
        print("post")
        for unit in order.units.all():
            box_cut_job = Box_Cut_Job.objects.filter(unit=unit).first()
            
            if box_cut_job:

                form = BoxCutJobForm(request.POST, instance=box_cut_job, prefix=str(unit.id))
            else:

                # Create a new Box_Cut_Job instance with default values
                box_cut_job = Box_Cut_Job(unit=unit)
                form = BoxCutJobForm(request.POST, instance=box_cut_job, prefix=str(unit.id))

            unitforms[unit.unit_number] = form
            if form.is_valid():
                instance = form.save(commit=False)
                instance.unit = unit
                instance.save()
            else:
                print(form.errors)

        return render(request, "workstation/box_cut.html", {'unitforms': unitforms, 'order': order, 'totalunits':totalunits})

    else:
        print("get")
        for unit in order.units.all():
            box_cut_job = Box_Cut_Job.objects.filter(unit=unit).first()
            if box_cut_job:
                form = BoxCutJobForm(instance=box_cut_job, prefix=str(unit.id))
            else:
                # Create a new Box_Cut_Job instance with default values
       
                box_cut_job = Box_Cut_Job(unit=unit)
                box_cut_job.save()  # Save the new instance with default values
                form = BoxCutJobForm(instance=box_cut_job, prefix=str(unit.id))

            unitforms[unit.unit_number] = form
            
    order_complete = True
    for unit in order.units.all():
        box_cut_job = Box_Cut_Job.objects.filter(unit=unit).first()
        if not box_cut_job.job_complete:
            order_complete =False
    if order_complete:
        return render(request, "workstation/job_complete.html", {"po_number":order.po_number})
        

    return render(request, "workstation/box_cut.html", {'unitforms': unitforms, 'order': order, 'totalunits':totalunits})

def confirm_box_cut(request, po_number):
    order = get_object_or_404(Order, po_number=po_number)
    units = order.units.all()
    
    print("METHOD POST")
    if request.method == 'POST':
        for unit in units:
            box_cut_job = Box_Cut_Job.objects.filter(unit=unit).first()
            print(box_cut_job)
            if box_cut_job:
                box_cut_job.job_complete = True
                box_cut_job.box_cut_drop_used = True
                box_cut_job.box_cut_hd_box = True
                box_cut_job.box_cut_cut_length = True
                box_cut_job.box_prep_track_notch = True
                box_cut_job.box_prep_drill_holes_top_back = True
                box_cut_job.box_prep_drill_holes_front_bottom = True
                box_cut_job.hem_bar_drop_used = True
                box_cut_job.hem_bar_hd_hem_bar = True
                box_cut_job.hem_bar_cut_length = True
                box_cut_job.hem_bar_drill_end_cap_screws = True
                box_cut_job.hem_bar_drill_hook_hole = True
                box_cut_job.tracks_drop_used = True
                box_cut_job.tracks_hd_tracks = True
                box_cut_job.tracks_cut_length = True
                box_cut_job.tracks_drill_mounting_holes = True
                box_cut_job.tracks_drill_hook_hole = True
                box_cut_job.tube_drop_used = True
                box_cut_job.tube_length = True
                box_cut_job.tube_cut_length = True
                box_cut_job.l_channel_drop_used = True
                box_cut_job.l_channel_quantity = True
                box_cut_job.l_channel_cut_length = True
                box_cut_job.l_channel_drill_hook_hole = True
                box_cut_job.save()
        

    return redirect('workstation_dashboard')  
        

def tube_cut(request):
    return render(request,"workstation/box_cut.html")

def track_prep(request):
    return render(request,"workstation/box_cut.html")

def hardware(request):
    return render(request,"workstation/box_cut.html")

def powder_coat(request):
    return render(request,"workstation/box_cut.html")

def fabric(request):
    return render(request,"workstation/box_cut.html")

def assembly(request):
    return render(request,"workstation/box_cut.html")

def shipping(request):
    return render(request,"workstation/box_cut.html")